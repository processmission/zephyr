.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _tls_credentials_shell:

TLS 凭据 shell
##############

TLS 凭据 shell 提供了用于管理已安装 TLS 凭据的命令行界面。

命令
****

.. _tls_credentials_shell_buf_cred:

缓冲凭据（``buf``）
===================

将数据逐步缓冲到凭据缓冲区，以便随后使用 :ref:`tls_credentials_shell_add_cred` 命令添加。

或者：

   - 清空凭据缓冲区。

   - 直接将凭据加载到凭据缓冲区，以 ``Ctrl + c`` 结束。

用法
----

要将 ``<DATA>`` 追加到凭据缓冲区，请使用：

.. code-block:: shell

   cred buf <DATA>

根据需要多次执行该命令，将完整凭据加载到凭据缓冲区，然后使用 :ref:`tls_credentials_shell_add_cred` 命令将其存储。

要将 ``<DATA>`` 直接加载到凭据缓冲区，请使用：

.. code-block:: shell

   cred buf load
   <DATA>
   Ctrl + c

要清空凭据缓冲区，请使用：

.. code-block:: shell

   cred buf clear

参数
----

.. csv-table::
   :header: "参数", "描述"
   :widths: 15 85

   "``<DATA>``", "要追加到凭据缓冲区的文本数据。它可以是文本，也可以是 base64 编码的二进制数据。详情见 :ref:`tls_credentials_shell_add_cred` 和 :ref:`tls_credentials_shell_data_formats`。"

.. _tls_credentials_shell_add_cred:

添加凭据（``add``）
===================

将 TLS 凭据添加到 TLS 凭据存储中。

凭据内容可以在调用 ``cred add`` 时内联提供，否则将从凭据缓冲区中读取。

Usage
-----

要使用凭据缓冲区中的数据添加 TLS 凭据，请使用：

.. code-block:: shell

   cred add <SECTAG> <TYPE> <BACKEND> <FORMAT>

要使用同一命令中提供的数据添加 TLS 凭据，请使用：

.. code-block:: shell

   cred add <SECTAG> <TYPE> <BACKEND> <FORMAT> <DATA>


Arguments
---------

.. csv-table::
   :header: "Argument", "Description"
   :widths: 15 85

   "``<SECTAG>``", "用于新凭据的 sectag（安全标签）。可以是任意非负整数。"
   "``<TYPE>``", "要添加的凭据类型。有效值见 :ref:`tls_credentials_shell_cred_types`。"
   "``<BACKEND>``", "保留。必须始终为 ``DEFAULT`` （不区分大小写）。"
   "``<FORMAT>``", "指定所提供凭据的存储格式。有效值见 :ref:`tls_credentials_shell_data_formats`。"
   "``<DATA>``", "如果提供，此参数将用作凭据数据，而不是凭据缓冲区中的任何数据。它可以是文本，也可以是 base64 编码的二进制数据。"

.. _tls_credentials_shell_del_cred:

删除凭据（``del``）
===================

从凭据存储中删除指定的凭据。

Usage
-----

要删除与指定 sectag 和凭据类型匹配的凭据（如果存在），请使用：

.. code-block:: shell

   cred del <SECTAG> <TYPE>

Arguments
---------

.. csv-table::
   :header: "Argument", "Description"
   :widths: 15 85

   "``<SECTAG>``", "要删除凭据的 sectag。可以是任意非负整数。"
   "``<TYPE>``", "要删除的凭据类型。有效值见 :ref:`tls_credentials_shell_cred_types`。"

.. _tls_credentials_shell_get_cred:

获取凭据内容（``get``）
=======================

检索并打印指定凭据的内容。

Usage
-----

要检索并打印与指定 sectag 和凭据类型匹配的凭据（如果存在），请使用：

.. code-block:: shell

   cred get <SECTAG> <TYPE> <FORMAT>

Arguments
---------

.. csv-table::
   :header: "Argument", "Description"
   :widths: 15 85

   "``<SECTAG>``", "要获取凭据的 sectag。可以是任意非负整数。"
   "``<TYPE>``", "要获取的凭据类型。有效值见 :ref:`tls_credentials_shell_cred_types`。"
   "``<FORMAT>``", "指定所提供凭据的检索格式。有效值见 :ref:`tls_credentials_shell_data_formats`。"

.. _tls_credentials_shell_list_cred:

列出凭据（``list``）
====================

列出凭据存储中的 TLS 凭据。

Usage
-----

要列出所有可用凭据，请使用：

.. code-block:: shell

   cred list

要列出具有指定 sectag 的所有凭据，请使用：

.. code-block:: shell

   cred list <SECTAG>

要列出具有指定凭据类型的所有凭据，请使用：

.. code-block:: shell

   cred list any <TYPE>

要列出同时具有指定凭据类型和 sectag 的所有凭据，请使用：

.. code-block:: shell

   cred list <SECTAG> <TYPE>


Arguments
---------

.. csv-table::
   :header: "Argument", "Description"
   :widths: 15 85

   "``<SECTAG>``", "可选。如果提供，则仅列出具有此 sectag 的凭据。传入 ``any`` 或省略以允许任意 sectag。否则可以是任意非负整数。"
   "``<TYPE>``", "可选。如果提供，则仅列出具有此凭据类型的凭据。传入 ``any`` 或省略以允许任意凭据类型。否则，有效值见 :ref:`tls_credentials_shell_cred_types`。"


输出
----

该命令按以下（符合 CSV 的）格式输出所有匹配的凭据：

.. code-block:: shell

   <SECTAG>,<TYPE>,<DIGEST>,<STATUS>

位置：

.. csv-table::
   :header: "符号", "值"
   :widths: 15 85

   "``<SECTAG>``", "所列凭据的 sectag。非负整数。"
   "``<TYPE>``", "所列凭据的类型短代码（详情见 :ref:`tls_credentials_shell_cred_types`）。"
   "``<DIGEST>``", "表示凭据内容的字符串摘要。摘要的具体形式可能因凭据存储后端而异，但目前所有后端都使用原始凭据内容的 base64 编码 SHA256 哈希（因此，实质相同的凭据采用不同存储格式时，摘要也会不同）。"
   "``<STATUS>``", "状态码，表示生成所列凭据摘要的成功或失败情况。成功时为 0，否则为存储后端特定的负错误码。状态不为零的行将以错误格式打印。"

列表打印完成后，将以如下形式打印所找到凭据的最终汇总：

.. code-block:: shell

   <N> credentials found.

其中 ``<N>`` 是找到的凭据数量，如果未找到任何凭据则为零。

.. _tls_credentials_shell_cred_types:

凭据类型
********

可以使用以下关键字（不区分大小写）来指定凭据类型：

.. csv-table::
   :header: "关键字", "含义"
   :widths: 15 85

   "``CA_CERT``, ``CA``", "受信任的 CA 证书。"
   "``SERVER_CERT``, ``SELF_CERT``, ``CLIENT_CERT``, ``CLIENT``, ``SELF``, ``SERV``", "自身证书或服务器证书。"
   "``PRIVATE_KEY``, ``PK``", "私钥。"
   "``PRE_SHARED_KEY``, ``PSK``", "预共享密钥。"
   "``PRE_SHARED_KEY_ID``, ``PSK_ID``", "预共享密钥的 ID。"

.. _tls_credentials_shell_data_formats:

存储/检索格式
*************

:ref:`tls_credentials <sockets_tls_credentials_subsys>` 模块将存储的凭据视为任意二进制缓冲区。

为方便起见，TLS 凭据 shell 提供了四种格式，以便通过 shell 提供这些缓冲区并在稍后检索它们。

这些格式及其关键字（不区分大小写）如下：

.. csv-table::
   :header: "关键字", "Meaning", "存储时的行为（``cred add``）", "检索时的行为（``cred get``）"
   :widths: 3, 32, 34, 34

   "``BIN``", "shell 将凭据作为 base64 处理，存储时不添加 NULL 终止符。", "输入到 shell 的数据在存储前会从 base64 解码为原始二进制。不会追加终止符。", "存储的数据在打印前会编码为 base64。"
   "``BINT``", "shell 将凭据作为 base64 处理，存储时添加 NULL 终止符。", "输入到 shell 的数据会从 base64 解码为原始二进制，并在存储前追加一个 NULL 终止符。", "在将存储的数据编码为 base64 并打印之前，会先从中截除 NULL 终止符。"
   "``STR``", "shell 将凭据作为字面字符串处理，存储时不添加 NULL 终止符。", "输入到 shell 的文本数据会按原样传入存储，不添加 NULL 终止符。", "存储的数据将作为文本打印。不可打印字符将打印为 ``?``"
   "``STRT``", "shell 将凭据作为字面字符串处理，存储时添加 NULL 终止符。", "输入到 shell 的文本数据会按原样传入存储，并添加一个 NULL 终止符。", "在将存储的数据作为文本打印之前，会先从中截除 NULL 终止符。不可打印字符将打印为 ``?``"

``BIN`` 格式可用于安装任意类型的凭据，因为 base64 可用来编码任何可以想到的二进制缓冲区。其余三种格式则是为了方便特殊用例而提供的。

例如：

- 要安装可打印的预共享密钥，请使用 ``STR`` 输入 PSK，而无需预先编码。这样可以确保存储时不添加 NULL 终止符。
- 要安装 DER 格式的 X.509 证书（或其他原始二进制凭据，例如不可打印的 PSK），请对二进制数据进行 base64 编码并使用 ``BIN`` 格式。
- 要安装 PEM 格式的 X.509 证书或证书链，请对整个 PEM 字符串（包括换行符以及 ``----BEGIN X ----`` / ``----END X----`` 标记）进行 base64 编码，然后使用 ``BINT`` 格式，以确保存储的字符串以 NULL 结尾。之所以需要这样做，是因为 Zephyr 的 shell 不支持多行字符串。否则，可以为此使用 ``STRT`` 格式，而无需进行 base64 编码。如果手动将 NULL 终止符编码到 base64 中，也可以改用 ``BIN``。
