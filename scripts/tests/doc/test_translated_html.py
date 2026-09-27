# SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
# SPDX-License-Identifier: Apache-2.0

import io
import json

from sphinx.application import Sphinx

from doc._scripts.package_translations import package


def test_only_translations_are_rendered_and_indexed(tmp_path):
    source = tmp_path / 'source'
    translated = tmp_path / 'translations'
    output = tmp_path / 'html'
    source.mkdir()
    translated.mkdir()
    (translated / 'index.rst').write_text('中文\n====\n')
    (source / 'index.rst').write_text(
        '中文\n====\n\n.. toctree::\n\n   english\n\n:ref:`英文参考 <english-topic>`\n'
    )
    (source / 'english.rst').write_text(
        '.. _english-topic:\n\nEnglish reference\n=================\n'
    )
    (source / 'conf.py').write_text(
        "extensions = ['doc._extensions.zephyr.translated_html']\n"
        "language = 'zh_CN'\n"
        "html_baseurl = 'https://example.com/zephyr/'\n"
        "def setup(app):\n"
        f"    app.add_config_value('external_content_overlay', {str(translated)!r}, 'env')\n"
        "    app.add_config_value('html_redirect_pages', "
        "[('legacy/topic', 'english'), ('older/topic', 'legacy/topic'), "
        "('legacy/home', 'index')], '')\n"
    )
    warnings = io.StringIO()
    app = Sphinx(
        str(source),
        str(source),
        str(output),
        str(tmp_path / 'doctrees'),
        'html',
        status=io.StringIO(),
        warning=warnings,
        warningiserror=True,
    )
    app.build(force_all=True)
    assert app.statuscode == 0, warnings.getvalue()
    assert not (output / 'english.html').exists()
    assert (
        'https://docs.zephyrproject.org/latest/english.html#english-topic'
        in (output / 'index.html').read_text()
    )
    assert tuple(app.builder.indexer.freeze()['docnames']) == ('index',)
    manifest = json.loads((output / '_translated_pages.json').read_text())
    assert 'english.html' in manifest['upstream_pages']
    assert 'english.html' not in manifest['pages']
    assert manifest['redirects']['older/topic.html'] == (
        'https://docs.zephyrproject.org/latest/english.html'
    )
    assert app.builder.get_relative_uri('guide/page', 'legacy/home') == '../index.html'
    published = tmp_path / 'published'
    package(output, published)
    assert (
        'https://docs.zephyrproject.org/latest/english.html'
        in (published / 'older/topic.html').read_text()
    )
    assert '../index.html' in (published / 'legacy/home.html').read_text()


def test_publication_routes_raw_links_and_excludes_english_payloads(tmp_path):
    source = tmp_path / 'html'
    output = tmp_path / 'site'
    (source / 'guide').mkdir(parents=True)
    (source / '_static').mkdir()
    (source / '_images').mkdir()
    (source / 'doxygen/html').mkdir(parents=True)
    (source / '_translated_pages.json').write_text(
        json.dumps(
            {
                'pages': ['guide/index.html'],
                'upstream_pages': ['boards/index.html'],
                'site_base_url': 'https://example.com/zephyr/',
                'upstream_base_url': 'https://docs.zephyrproject.org/latest/',
            }
        )
    )
    (source / 'guide/index.html').write_text(
        '<a href="/zephyr/doxygen/html/api.html#symbol">API</a>'
        '<a href="../boards/">Boards</a><img src="../_images/photo.png">'
        '<a href="https://other.example/boards/">External</a>'
    )
    (source / 'doxygen/html/api.html').write_text('ENGLISH API PAYLOAD')
    (source / '_images/photo.png').write_bytes(b'image')
    (source / '_static/app.js').write_text('window.example = true;')
    (source / '_static/app.js.map').write_text('debug source map')
    (source / '_static/loop').symlink_to(source, target_is_directory=True)
    package(source, output)
    page = (output / 'guide/index.html').read_text()
    assert 'https://docs.zephyrproject.org/latest/doxygen/html/api.html#symbol' in page
    assert 'https://docs.zephyrproject.org/latest/boards/' in page
    assert '../_images/photo.png' in page
    assert 'https://other.example/boards/' in page
    assert (output / '_images/photo.png').read_bytes() == b'image'
    assert not (output / 'en').exists()
    assert not (output / '_static/app.js.map').exists()
    assert not (output / '_static/loop').exists()
    redirect = (output / 'boards/index.html').read_text()
    assert 'location.search+location.hash' in redirect
    assert 'https://docs.zephyrproject.org/latest/boards/index.html' in redirect
    assert 'ENGLISH API PAYLOAD' not in (output / 'doxygen/html/api.html').read_text()
