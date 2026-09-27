.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

蓝牙：经典：PBAP Shell
######################

本文档介绍如何运行蓝牙经典 PBAP（电话簿访问配置文件）功能。 :code:`pbap` 命令提供蓝牙经典 PBAP Shell 命令。

有两个子命令： :code:`pbap pce` 和 :code:`pbap pse`。

:code:`pbap pce` 用于电话簿客户端设备（PCE）功能， :code:`pbap pse` 用于电话簿服务器设备（PSE）功能。

命令
****

除 :code:`pbap pce sdp_reg`、 :code:`pbap pse rfcomm_register` 和 :code:`pbap pse l2cap_register` 之外，所有命令都只能在建立 ACL 连接后使用。

:code:`pbap` 命令：

.. code-block:: console

   uart:~$ pbap
   pbap - Bluetooth pbap shell commands
   Subcommands:
     alloc_buf                        : Alloc tx buffer
     release_buf                      : Free allocated tx buffer
     pce                              : Client sets
     pse                              : Server sets
     add_header_auth_challenge        : <password>
     add_header_auth_response         : <password>
     add_ap                           : add application param

:code:`pbap pce` 命令：

.. code-block:: console

   uart:~$ pbap pce
   pce - Client sets
   Subcommands:
     sdp_reg                          : [none]
     sdp_discover                     : [none]
     connect_rfcomm                   : <channel>
     disconnect_rfcomm                : [none]
     connect_l2cap                    : <channel>
     disconnect_l2cap                 : [none]
     connect                          : <mopl>
     disconnect                       : [none]
     pull_pb                          : <name> [srmp]
     pull_vcard_listing               : <name> [srmp]
     pull_vcard_entry                 : <name> [srmp]
     set_phone_book                   : <Flags> [name]
     abort                            : [none]

:code:`pbap pse` 命令：

.. code-block:: console

   uart:~$ pbap pse
   pse - Server sets
   Subcommands:
     rfcomm_register                  : [none]
     l2cap_register                   : [none]
     register                         : [none]
     connect_rsp                      : <mopl> <rsp: unauth,success,error> [rsp_code]
     disconnect_rsp                   : <rsp: success,error> [rsp_code]
     pull_phone_book_rsp              : <rsp: noerror, error> [rsp_code] [srmp]
     pull_vcard_listing_rsp           : <rsp: noerror, error> [rsp_code] [srmp]
     pull_vcard_entry_rsp             : <rsp: noerror, error> [rsp_code] [srmp]
     set_phone_book_rsp               : <rsp: success, error> [rsp_code]
     abort_rsp                        : <rsp: success, error> [rsp_code]

:code:`pbap add_ap` （应用参数）命令：

.. code-block:: console

   uart:~$ pbap add_ap
   add_ap - add application param
   Subcommands:
     Order                            : <indexed/alphanumeric/phonetic>
     SearchValue                      : <text>
     SearchAttribute                  : <name/number/sound>
     MaxListCount                     : <0x0000-0xffff>
     ListStartOffset                  : <0x0000-0xffff>
     PropertySelector                 : <64 bits mask : bt_pbap_appl_param_property_mask>
     Format                           : <v2.1/v3.0>
     PhonebookSize                    : <0x0000-0xffff>
     NewMissedCalls                   : <0x00-0xff>
     PrimaryFolderVersion             : <16bytes>
     SecondaryFolderVersion           : <16bytes>
     vCardSelector                    : <64 bits mask : bt_pbap_appl_param_property_mask>
     DatabaseIdentifier               : <16bytes>
     vCardSelectorOperator            : <or/and>
     ResetNewMissedCalls              :
     PbapSupportedFeatures            : [supported features]

PBAP PCE SLC
************

:code:`pbap pce` 子命令提供蓝牙经典中 PBAP PCE（电话簿客户端设备）的功能。

1. 注册 PCE SDP：

.. code-block:: console

   uart:~$ pbap pce sdp_reg

2. 发现 PSE SDP：

.. code-block:: console

   uart:~$ pbap pce sdp_discover
   SDP PBAP data@0x2000d4a0 (len 54) hint 0 from remote XX:XX:XX:XX:XX:XX
   PSE rfcomm channel param 0x0001
   PSE l2cap psm param 0x0019
   PSE feature param 0x00000019

3. 通过 RFCOMM 连接到 PSE：

.. code-block:: console

   uart:~$ pbap pce connect_rfcomm 0x01
   PBAP PCE rfcomm transport connected on 0x20005dd8

4. 建立 OBEX 连接：

.. code-block:: console

   uart:~$ pbap alloc_buf
   uart:~$ pbap pce connect 300
   pbap connect result Success, mopl 256
   Connection ID: 0x00000001
   Processing successful connection...
   Connection established successfully (no auth required)

5. 断开与 PSE 的连接：

.. code-block:: console

   uart:~$ pbap pce disconnect
   pbap disconnect result OK
   PBAP PCE rfcomm transport disconnected

PBAP PSE SLC
************

:code:`pbap pse` 子命令提供蓝牙经典中 PBAP PSE（电话簿服务器设备）的功能。

1. 注册 PSE RFCOMM 服务器：

.. code-block:: console

   uart:~$ pbap pse rfcomm_register
   RFCOMM server (channel 01) is registered

2. 注册 PSE L2CAP 服务器：

.. code-block:: console

   uart:~$ pbap pse l2cap_register
   L2cap server (psm 01) is registered

3. 注册 PSE：

.. code-block:: console

   uart:~$ pbap pse register

4. 接受 PCE 连接并响应：

.. code-block:: console

   uart:~$ pbap alloc_buf
   uart:~$ pbap pse connect_rsp 300 success
   pbap connect version 1, mopl 256
   Connection established with authentication

5. 断开与 PCE 的连接：

.. code-block:: console

   uart:~$ pbap alloc_buf
   uart:~$ pbap pse disconnect_rsp success
   pbap disconnect requested by pce


拉取电话簿
**********

从 PSE 拉取完整电话簿：

.. tabs::

   .. group-tab:: PCE 侧

      .. code-block:: console

         uart:~$ pbap alloc_buf
         uart:~$ pbap pce pull_pb "telecom/pb"
         pbap pull phonebook result Continue
         Application Parameters (length: 2):
           PhonebookSize: 0x0002 (2)

         =========body=========
         BEGIN:VCARD
         VERSION:2.1
         FN;CHARSET=UTF-8:descvs
         N;CHARSET=UTF-8:descvs
         END:VCARD
         =========body=========

         please send pull cmd again
         uart:~$ pbap pce pull_pb "telecom/pb"
         pbap pull phonebook result Success
         Application Parameters (length: 2):
           PhonebookSize: 0x0002 (2)

         =========body=========
         BEGIN:VCARD
         VERSION:2.1
         FN;CHARSET=UTF-8:descvs
         N;CHARSET=UTF-8:descvs
         END:VCARD
         =========body=========

   .. group-tab:: PSE 侧

      .. code-block:: console

         uart:~$ pbap alloc_buf
         pbap_pse get pull_phone_book request
         name = telecom/pb
         Application Parameters (length: 0):

         uart:~$ pbap alloc_buf
         uart:~$ pbap pse pull_phone_book_rsp noerror
         Suspend after sending a single response and await the PCE request

         uart:~$ pbap alloc_buf
         uart:~$ pbap pse pull_phone_book_rsp noerror
         Keep sending responses continuously until rsp_code is success

拉取 vCard 列表
***************

拉取 vCard 列表以发现联系人：

.. tabs::

   .. group-tab:: PCE 侧

      .. code-block:: console

         uart:~$ pbap alloc_buf
         uart:~$ pbap add_ap MaxListCount 0x0005
         uart:~$ pbap add_ap ListStartOffset 0x0000
         uart:~$ pbap pce pull_vcard_listing "telecom/pb"
         pbap pull vcard_listing result Continue
         Application Parameters (length: 6):
           MaxListCount: 0x0005 (5)
           ListStartOffset: 0x0000 (0)

         =========body=========
         <?xml version="1.0"?><!DOCTYPE vcard-listing SYSTEM "vcard-listing.dtd">
         <vCard-listing version="1.0"><card handle="1.vcf" name="qwe"/>
         <card handle="2.vcf" name="qwe"/>
         =========body=========

         please send pull cmd again
         uart:~$ pbap pce pull_vcard_listing "telecom/pb"
         pbap pull vcard_listing result Success
         =========body=========
         <card handle="1.vcf" name="qwe"/><card handle="2.vcf" name="qwe"/>
         /<vCard-listing>
         =========body=========

   .. group-tab:: PSE 侧

      .. code-block:: console

         uart:~$ pbap alloc_buf
         pbap_pse get pull_vcard_listing request
         name = telecom/pb
         Application Parameters (length: 6):
           MaxListCount: 0x0005 (5)
           ListStartOffset: 0x0000 (0)

         uart:~$ pbap alloc_buf
         uart:~$ pbap pse pull_vcard_listing_rsp noerror
         Suspend after sending a single response and await the PCE request

         uart:~$ pbap alloc_buf
         uart:~$ pbap pse pull_vcard_listing_rsp noerror

拉取 vCard 条目
***************

拉取特定的 vCard 条目：

.. tabs::

   .. group-tab:: PCE 侧

      .. code-block:: console

         uart:~$ pbap alloc_buf
         uart:~$ pbap add_ap Format v2.1
         uart:~$ pbap pce pull_vcard_entry "telecom/pb/1.vcf"
         pbap pull vcard_entry result Continue
         Application Parameters (length: 1):
           Format: 0x00 (vCard 2.1)

         =========body=========
         BEGIN:VCARD
         VERSION:2.1
         FN:
         N:
         TEL;X-0:1155
         =========body=========

         uart:~$ pbap pce pull_vcard_entry "telecom/pb/1.vcf"
         pbap pull vcard_entry result Success

         =========body=========
         X-IRMC-CALL-DATETIME;DIALED:20220913T110607
         END:VCARD
         =========body=========

   .. group-tab:: PSE 侧

      .. code-block:: console

         uart:~$ pbap alloc_buf
         pbap_pse get pull_vcard_entry request
         name = telecom/pb/1.vcf
         Application Parameters (length: 1):
           Format: 0x00 (vCard 2.1)

         uart:~$ pbap alloc_buf
         uart:~$ pbap pse pull_vcard_entry_rsp noerror
         Suspend after sending a single response and await the PCE request

         uart:~$ pbap alloc_buf
         uart:~$ pbap pse pull_vcard_entry_rsp noerror

设置电话簿
**********

更改当前电话簿目录：

.. tabs::

   .. group-tab:: PCE 侧

      .. code-block:: console

         uart:~$ pbap alloc_buf
         uart:~$ pbap pce set_phone_book 0x02 "telecom"
         PBAP set phonebook result OK

         uart:~$ pbap alloc_buf
         uart:~$ pbap pce set_phone_book 0x02 "pb"
         PBAP set phonebook result OK

         uart:~$ pbap alloc_buf
         uart:~$ pbap pce set_phone_book 0x02
         PBAP set phonebook result OK

   .. group-tab:: PSE 侧

      .. code-block:: console

         uart:~$ pbap alloc_buf
         pbap_pse get set_phone_book request
         set phonebook to children telecom folder

         uart:~$ pbap alloc_buf
         uart:~$ pbap pse set_phone_book_rsp success

         uart:~$ pbap alloc_buf
         pbap_pse get set_phone_book request
         set phonebook to children pb folder

         uart:~$ pbap alloc_buf
         uart:~$ pbap pse set_phone_book_rsp success

         uart:~$ pbap alloc_buf
         pbap_pse get set_phone_book request
         set phonebook to parent folder

         uart:~$ pbap alloc_buf
         uart:~$ pbap pse set_phone_book_rsp success

中止操作
********

中止正在进行的操作：

.. tabs::

   .. group-tab:: PCE 侧

      .. code-block:: console

         uart:~$ pbap pce abort
         abort success.

   .. group-tab:: PSE 侧

      .. code-block:: console

         uart:~$ pbap alloc_buf
         pbap_pse get receive abort req

         uart:~$ pbap pse abort_rsp success

身份验证
********

PBAP 可以使用 OBEX 身份验证来实现安全连接。身份验证过程涉及质询-响应机制。

带身份验证质询的 PCE：

.. tabs::

   .. group-tab:: PCE 侧

      .. code-block:: console

         uart:~$ pbap alloc_buf
         uart:~$ pbap add_header_auth_challenge "password123"
         uart:~$ pbap pce connect 255
         pbap connect result Unauthorized, mopl 255
         PSE requires authentication
         Action required:
           1. Allocate new tx_buf (pbap alloc_buf)
           2. Add auth_response header (pbap add_header_auth_response <password>)
           3. Add original auth_challenge header (pbap add_header_auth_challenge <password>)
           4. Re-send connect request (pbap pce connect <mopl>)

         uart:~$ pbap alloc_buf
         uart:~$ pbap add_header_auth_response "password123"
         uart:~$ pbap add_header_auth_challenge "password123"
         uart:~$ pbap pce connect 255
         pbap connect result Success, mopl 255
         Connection ID: 0x00000001
         Authentication verified successfully
         Connection established with authentication

   .. group-tab:: PSE 侧

      .. code-block:: console

         uart:~$ pbap alloc_buf
         uart:~$ pbap pse register

         uart:~$ pbap alloc_buf
         pbap connect version 1, mopl 255
         PCE authentication required - add auth_response to connect_rsp tx_buf

         uart:~$ pbap alloc_buf
         uart:~$ pbap add_header_auth_challenge "password123"
         uart:~$ pbap pse connect_rsp 255 unauth

         uart:~$ pbap alloc_buf
         pbap connect version 1, mopl 255
         auth success
         Connection established with authentication

         uart:~$ pbap alloc_buf
         uart:~$ pbap pse connect_rsp 255 success
