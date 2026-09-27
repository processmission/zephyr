# SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
# SPDX-License-Identifier: Apache-2.0

"""Index Chinese prose without changing the spelling of technical identifiers."""

import hashlib
import json

from sphinx.application import Sphinx
from sphinx.search.zh import SearchChinese


class ChineseSearch(SearchChinese):
    # Sphinx 9's Chinese backend selects English stemmer code but refers to a
    # nonexistent ChineseStemmer constructor. Use matching identity stemmers on
    # both sides, preserving API identifiers as well as Chinese tokens.
    js_stemmer_rawcode = ""
    js_stemmer_code = """
var Stemmer = function () {
    this.stemWord = function (word) { return word.toLowerCase(); };
};
"""

    def stem(self, word: str) -> str:
        return word.lower()


def _search_page(app: Sphinx, pagename, _template, context, _doctree) -> None:
    if pagename != "search" or app.config.language != "zh_CN":
        return

    # Use Sphinx's fingerprinted script tags and invalidate the index URL when its
    # contents change, so browsers cannot combine an old index with a new tokenizer.
    app.add_js_file("language_data.js")
    app.add_js_file("searchtools.js")
    index = json.dumps(app.builder.indexer.freeze(), sort_keys=True).encode("utf-8")
    context["search_index_version"] = hashlib.sha256(index).hexdigest()[:12]


def setup(app: Sphinx) -> dict[str, bool]:
    app.add_search_language(ChineseSearch)
    app.connect("html-page-context", _search_page)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
