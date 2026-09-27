#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
# SPDX-License-Identifier: Apache-2.0

"""Publish Chinese HTML with links and compatibility redirects to upstream English docs."""

import argparse
import html
import json
import posixpath
import re
import shutil
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

URL_ATTRIBUTE = re.compile(
    r'(?P<head>\b(?:href|src|data|poster)=)(?P<quote>["\'])(?P<url>.*?)(?P=quote)'
)


def _redirect(target: str) -> str:
    escaped = html.escape(target, quote=True)
    script_target = json.dumps(target).replace('<', '\\u003c')
    return (
        '<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
        f'<meta http-equiv="refresh" content="0;url={escaped}">'
        f'<link rel="canonical" href="{escaped}"><title>上游英文文档</title>'
        f'<p>此页由上游英文站提供。<a href="{escaped}">打开英文文档</a></p>'
        f'<script>location.replace({script_target}+location.search+location.hash);</script>'
        '</html>\n'
    )


def package(source: Path, output: Path) -> int:
    """Publish only the local HTML pages recorded by the translated HTML builder."""
    source = source.resolve()
    output = output.resolve()
    if output == source or output.is_relative_to(source):
        raise ValueError('Output must be outside the input HTML directory')
    if output.exists():
        raise FileExistsError(f'Output directory already exists: {output}')
    manifest = json.loads((source / '_translated_pages.json').read_text(encoding='utf-8'))
    local_pages = set(manifest['pages'])
    upstream_pages = set(manifest['upstream_pages'])
    upstream = manifest['upstream_base_url'].rstrip('/') + '/'
    base = urlsplit(manifest['site_base_url'].rstrip('/') + '/')
    output.mkdir(parents=True)

    def ignored(directory: str, names: list[str]) -> set[str]:
        return {
            name
            for name in names
            if (Path(directory) / name).is_symlink()
            or name.endswith(('.js.map', '.mjs.map', '.css.map'))
        }

    for name in ('_static', '_images', '_downloads'):
        if (source / name).is_dir():
            shutil.copytree(source / name, output / name, ignore=ignored)
    for name in ('searchindex.js', 'objects.inv', 'sitemap.xml', 'sitemap_index.xml'):
        if (source / name).is_file():
            shutil.copyfile(source / name, output / name)

    def rewrite(value: str, page: str) -> str:
        url = urlsplit(html.unescape(value))
        if not url.path or url.scheme not in ('', 'http', 'https'):
            return value
        if url.netloc and url.netloc != base.netloc:
            return value
        path = unquote(url.path)
        if path.startswith('/'):
            if not path.startswith(base.path):
                return value
            target = posixpath.normpath(path[len(base.path) :])
        else:
            target = posixpath.normpath(posixpath.join(posixpath.dirname(page), path))
        document = target + '/index.html' if path.endswith('/') else target
        if document not in upstream_pages and not target.startswith('doxygen/'):
            return value
        if path.endswith('/'):
            target += '/'
        return html.escape(
            urlunsplit(
                (*urlsplit(upstream + quote(target, safe='/'))[:3], url.query, url.fragment)
            ),
            quote=True,
        )

    for relative in sorted(local_pages):
        path = output / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        text = (source / relative).read_text(encoding='utf-8')
        text = URL_ATTRIBUTE.sub(
            lambda m, page=relative: m['head'] + m['quote'] + rewrite(m['url'], page) + m['quote'],
            text,
        )
        path.write_text(text, encoding='utf-8')

    # Keep old local links usable without storing or rendering an English mirror.
    upstream_pages |= {
        path.relative_to(source).as_posix()
        for path in (source / 'doxygen').rglob('*.html')
        if not path.is_symlink()
    }
    for relative in sorted(upstream_pages - local_pages):
        path = output / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_redirect(upstream + quote(relative, safe='/')), encoding='utf-8')

    for relative, target in manifest.get('redirects', {}).items():
        if not urlsplit(target).scheme:
            target = posixpath.relpath(target, posixpath.dirname(relative) or '.')
        path = output / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_redirect(target), encoding='utf-8')

    (output / '.nojekyll').touch()
    size = sum(path.stat().st_size for path in output.rglob('*') if path.is_file())
    if size > 1_000_000_000:
        raise ValueError(f'Published site exceeds the GitHub Pages limit: {size:,} bytes')
    print(
        f'{len(local_pages)} local pages; {len(upstream_pages - local_pages)} upstream redirects; '
        f'{size / 1024**2:.1f} MiB published; no English mirror'
    )
    return size


def main() -> None:
    parser = argparse.ArgumentParser(allow_abbrev=False, description=__doc__)
    parser.add_argument('--html', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    package(args.html, args.output)


if __name__ == '__main__':
    main()
