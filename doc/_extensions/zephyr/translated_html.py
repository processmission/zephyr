# SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
# SPDX-License-Identifier: Apache-2.0

"""Render translated articles and link other documents to the official English site."""

import json
import shutil
from pathlib import Path

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.config import Config
from sphinx.util.osutil import relative_uri


class TranslatedHTMLBuilder(StandaloneHTMLBuilder):
    def init(self) -> None:
        root = Path(self.config.external_content_overlay)
        self.translated_pages = {
            path.relative_to(root).with_suffix('').as_posix() for path in root.rglob('*.rst')
        }
        self.translated_pages -= {'README', 'kconfig', 'develop/manifest/index'}
        super().init()

    def is_local(self, docname: str) -> bool:
        return (
            docname in self.translated_pages
            or docname in {'index', 'search', 'gsearch', '404'}
            or docname.startswith('genindex')
        )

    def get_target_uri(self, docname: str, typ: str | None = None) -> str:
        redirects = dict(self.config.html_redirect_pages)
        visited = set()
        while docname in redirects:
            if docname in visited:
                raise ValueError(f'Cyclic documentation redirect: {docname}')
            visited.add(docname)
            docname = redirects[docname]
        if not self.is_local(docname):
            return f'{self.config.translation_upstream_base_url}{docname}.html'
        return super().get_target_uri(docname, typ)

    def get_relative_uri(self, from_: str, to: str, typ: str | None = None) -> str:
        target = self.get_target_uri(to, typ)
        if target.startswith(('https://', 'http://')):
            return target
        return relative_uri(super().get_target_uri(from_, typ), target)

    def write_doc_serialized(self, docname: str, doctree: nodes.document) -> None:
        if self.is_local(docname):
            super().write_doc_serialized(docname, doctree)

    def write_doc(self, docname: str, doctree: nodes.document) -> None:
        if self.is_local(docname):
            super().write_doc(docname, doctree)


def _configure(app: Sphinx, config: Config) -> None:
    if config.language == 'zh_CN':
        app.add_builder(TranslatedHTMLBuilder, override=True)


def _manifest(app: Sphinx, exception: Exception | None) -> None:
    if exception is not None or not isinstance(app.builder, TranslatedHTMLBuilder):
        return
    builder = app.builder
    if builder.is_local('boards/index'):
        domain = app.env.domaindata.get('zephyr', {})
        for kind in ('boards', 'shields'):
            for item in domain.get(kind, {}).values():
                if image := item.get('image'):
                    source = Path(app.srcdir) / image
                    target = Path(app.outdir) / '_images' / 'catalog' / image
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source, target)
    local = {name for name in app.env.found_docs if builder.is_local(name)}
    local |= {'search', 'gsearch', 'genindex', '404'}
    local |= {path.stem for path in Path(app.outdir).glob('genindex*.html')}
    local |= {old for old, new in app.config.html_redirect_pages if builder.is_local(new)}
    document = {
        'pages': sorted(
            f'{name}.html' for name in local if (Path(app.outdir) / f'{name}.html').is_file()
        ),
        'upstream_pages': sorted(
            f'{name}.html' for name in app.env.found_docs if not builder.is_local(name)
        ),
        'redirects': {
            f'{old}.html': builder.get_target_uri(new)
            for old, new in app.config.html_redirect_pages
        },
        'upstream_base_url': app.config.translation_upstream_base_url,
        'site_base_url': app.config.html_context.get('docs_site_base_url', app.config.html_baseurl),
    }
    (Path(app.outdir) / '_translated_pages.json').write_text(json.dumps(document, indent=2) + '\n')


def setup(app: Sphinx) -> dict[str, bool]:
    app.add_config_value(
        'translation_upstream_base_url', 'https://docs.zephyrproject.org/latest/', 'html'
    )
    app.connect('config-inited', _configure, priority=950)
    app.connect('build-finished', _manifest)
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
