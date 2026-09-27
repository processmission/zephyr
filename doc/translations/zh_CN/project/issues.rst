.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _bug_reporting:

缺陷报告
########

为保持提案、变更、功能和问题之间的可追溯性及关联，建议在源代码提交与相关 GitHub 问题之间建立双向引用。凡是源于已跟踪功能或问题的变更，都应通过注明相应的问题或拉取请求标识符来引用该功能。

在任何时候，都应能够通过代码中的引用追溯变更的来源及其原因。

报告回归问题
************

如果已知某个用例在较早的提交或发布版本中能够正常运行，那么所报告的问题可能会被认定为回归问题。在这种情况下，提交缺陷报告时直接提供引入问题的提交，可以大幅节省后续修复缺陷所需的时间。

定位引入回归问题的提交有多种方法，其中，对代码树进行二分查找是一种高效的方法，无需深入了解代码，任何人都可以使用。

为此，推荐使用 `git bisect`_ 工具。

操作过程建议：

* 在二分查找的每一步运行 ``west update`` 。
* 二分查找结束并定位到引入问题的提交后，手动验证结果。

.. _git bisect:
   https://git-scm.com/docs/git-bisect
