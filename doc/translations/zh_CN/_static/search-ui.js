/* SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
 * SPDX-License-Identifier: Apache-2.0
 */
Documentation.addTranslations({
    locale: "zh_CN",
    plural_expr: "0",
    messages: {
        "Search Results": "搜索结果",
        "Searching": "正在搜索",
        "Preparing search...": "正在准备搜索……",
        ", in ": "，位于 ",
        ["Your search did not match any documents. Please make sure that all words " +
         "are spelled correctly and that you've selected enough categories."]:
            "没有找到匹配文档，请检查关键词拼写或换用其他关键词。",
        "Search finished, found one page matching the search query.":
            ["搜索完成，找到 ${resultCount} 个匹配页面。"],
    },
});

document.addEventListener("DOMContentLoaded", function () {
    const link = document.getElementById("upstream-search");
    if (link) {
        const url = new URL(link.href);
        url.search = window.location.search;
        link.href = url.href;
    }
});
