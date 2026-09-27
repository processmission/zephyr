# SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
# SPDX-License-Identifier: Apache-2.0

import os
from types import SimpleNamespace

from doc._extensions.zephyr.external_content import DEFAULT_DIRECTIVES, sync_contents


def test_translation_selection_and_include_paths(tmp_path):
    original = tmp_path / 'doc'
    overlay = original / 'translations' / 'zh_CN'
    output = tmp_path / 'build'
    overlay.mkdir(parents=True)
    output.mkdir()
    english = 'English\n=======\n\n.. include:: shared.rst\n\n.. literalinclude:: example.c\n'
    (original / 'index.rst').write_text(english)
    (original / 'shared.rst').write_text('Shared English text.\n')
    (original / 'example.c').write_text('int example;\n')
    translated = '中文\n====\n\n.. include:: shared.rst\n\n.. literalinclude:: example.c\n'
    (overlay / 'index.rst').write_text(translated)
    (overlay / 'shared.rst').write_text('共用说明。\n')
    app = SimpleNamespace(
        srcdir=output,
        config=SimpleNamespace(
            external_content_contents=[(original, '*')],
            external_content_keep=[],
            external_content_exclude=[original / 'translations'],
            external_content_overlay='',
            external_content_directives=DEFAULT_DIRECTIVES,
            source_encoding='utf-8',
        ),
    )

    sync_contents(app)
    assert (output / 'index.rst').read_text().startswith('English\n')
    assert not (output / 'translations').exists()

    app.config.external_content_overlay = str(overlay)
    os.utime(overlay / 'index.rst', (1, 1))
    sync_contents(app)
    assembled = (output / 'index.rst').read_text()
    assert assembled.startswith('中文\n')
    assert '.. include:: shared.rst' in assembled
    code_path = next(
        line.split(':: ', 1)[1]
        for line in assembled.splitlines()
        if line.startswith('.. literalinclude::')
    )
    assert (output / code_path).resolve() == original / 'example.c'
    assert (output / 'shared.rst').read_text() == '共用说明。\n'

    (overlay / 'index.rst').write_text(translated.replace('中文', '更新'))
    os.utime(overlay / 'index.rst', (1, 1))
    sync_contents(app)
    assert (output / 'index.rst').read_text().startswith('更新\n')

    (overlay / 'index.rst').unlink()
    sync_contents(app)
    assert (output / 'index.rst').read_text().startswith('English\n')
    assert (original / 'index.rst').read_text() == english

    (original / 'example.c').unlink()
    sync_contents(app)
    assert not (output / 'example.c').exists()
