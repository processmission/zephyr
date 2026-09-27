/* SPDX-FileCopyrightText: Copyright The Process Mission
 * SPDX-License-Identifier: Apache-2.0
 */
window.ZEPHYR_CATALOG_TRANSLATIONS = {
    "Switch to Card View": "切换为卡片视图",
    "Switch to Compact View": "切换为紧凑视图",
    "Showing {boards} of {totalBoards} boards, {shields} of {totalShields} shields":
        "显示 {boards} / {totalBoards} 个开发板，{shields} / {totalShields} 个扩展板",
    "Minimum on-target {type}": "目标 {type} 最小容量",
    "Maximum on-target {type}": "目标 {type} 最大容量",
    "Any": "不限",
};

document.addEventListener("DOMContentLoaded", function () {
    for (const field of document.querySelectorAll(".cs-search-input")) {
        field.placeholder = "筛选代码示例……";
        field.setAttribute("aria-label", "筛选代码示例");
    }
});
