# SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
from types import SimpleNamespace

from anytree import Resolver


def test_parallel_merge_does_not_restore_stale_sample_translations(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).parents[3] / 'doc' / '_extensions'))
    from zephyr.domain import ZephyrDomain

    current = ZephyrDomain(SimpleNamespace(domaindata={}))
    worker = ZephyrDomain(SimpleNamespace(domaindata={}))
    category_doc = 'samples/application/index'
    sample_doc = 'samples/application/hello/README'
    for domain, name in ((current, '应用开发'), (worker, 'Application Development')):
        domain.add_code_sample_category(
            {'id': 'application', 'name': name, 'docname': category_doc}
        )
        domain.add_code_sample({'id': 'hello', 'name': name, 'docname': sample_doc})

    worker.add_code_sample_category({'id': 'new', 'name': '新分类', 'docname': 'samples/new/index'})
    worker.add_code_sample(
        {'id': 'new_sample', 'name': '新示例', 'docname': 'samples/new/demo/README'}
    )
    current.merge_domaindata(['samples/new/index', 'samples/new/demo/README'], worker.data)

    assert current.data['code-samples-categories']['application']['name'] == '应用开发'
    assert current.data['code-samples']['hello']['name'] == '应用开发'
    tree = current.data['code-samples-categories-tree']
    assert Resolver().get(tree, '/samples/application').category['name'] == '应用开发'
    assert Resolver().get(tree, '/samples/new').category['name'] == '新分类'
    assert current.data['code-samples']['new_sample']['name'] == '新示例'
