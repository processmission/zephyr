.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_requests:

requests
########

简介
****

`requests`_ 提供易用接口，通过 Zephyr 网络协议栈执行 GET、POST、PUT、DELETE 等常见 HTTP(S) 操作。它还内置 shell 命令，可直接从 Zephyr shell 与 HTTP(S) 端点交互。

.. code-block:: shell

   uart:~$ requests
   requests - HTTP requests commands
   Subcommands:
     get     : Perform HTTP GET request
               Usage: get <url>
     post    : Perform HTTP POST request
               Usage: post <url> <body>
     put     : Perform HTTP PUT request
               Usage: put <url> <body>
     delete  : Perform HTTP DELETE request
               Usage: delete <url>
   uart:~$

在 Zephyr 中使用
****************

要将 requests 作为 Zephyr 模块引入，可以在 :file:`west.yaml` 中将其添加为 West 项目，也可以添加包含以下内容的子清单文件，例如 ``zephyr/submanifests/requests.yaml``，然后运行 :command:`west update`：

.. code-block:: yaml

   manifest:
     projects:
       - name: requests
         url: https://github.com/walidbadar/requests.git
         revision: main
         path: modules/lib/requests # adjust the path as needed

API 细节见 ``requests`` 头文件。

参考资料
********

.. target-notes::

.. _requests: https://github.com/walidbadar/requests
