.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _mcumgr_callbacks:

MCUmgr 回调
###########

概述
****

MCUmgr 具有可定制的回调/通知系统，允许应用程序（和模块）代码接收其感兴趣的 MCUmgr 事件的回调，并对这些事件作出反应，或向调用函数返回状态码，从而控制是否应允许该操作。fs_mgmt 组就是一个例子：文件访问可以被门控，回调允许应用程序检查请求路径并允许或拒绝对该文件的访问，或者可以将提供的路径重写为其他路径，以支持透明文件重定向。

实现
****

启用
====

可以使用 :kconfig:option:`CONFIG_MCUMGR_MGMT_NOTIFICATION_HOOKS` 启用基础回调/通知系统，这会将注册和通知系统编译到代码中。默认情况下，这不会提供任何回调，因为构建所支持的回调还必须通过为所需回调启用相应的 Kconfig 来选择（有关更多详细信息，请参阅 :ref:`mcumgr_cb_events`）。然后可以声明一个使用 :c:type:`mgmt_cb` 类型定义的回调函数，并通过在 :c:struct:`mgmt_callback` 结构体内为所需事件调用 :c:func:`mgmt_callback_register` 来注册该函数。处理程序按注册顺序调用。

启用该系统后，可以按照如下方式在应用程序代码中设置并定义基本处理程序：

.. code-block:: c

    #include <zephyr/kernel.h>
    #include <zephyr/mgmt/mcumgr/mgmt/mgmt.h>
    #include <zephyr/mgmt/mcumgr/mgmt/callbacks.h>

    struct mgmt_callback my_callback;

    enum mgmt_cb_return my_function(uint32_t event, enum mgmt_cb_return prev_status,
                                    int32_t *rc, uint16_t *group, bool *abort_more,
                                    void *data, size_t data_size)
    {
        if (event == MGMT_EVT_OP_CMD_DONE) {
            /* This is the event we registered for */
        }

        /* Return OK status code to continue with acceptance to underlying handler */
        return MGMT_CB_OK;
    }

    int main()
    {
        my_callback.callback = my_function;
        my_callback.event_id = MGMT_EVT_OP_CMD_DONE;
        mgmt_callback_register(&my_callback);
    }

此代码为 :c:enumerator:`MGMT_EVT_OP_CMD_DONE` 事件注册一个处理程序，该处理程序将在 MCUmgr 命令处理完并生成输出后调用；请注意，这需要启用 :kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS` 才能接收此回调。

可以设置多个回调使用同一个函数作为公共回调；也可以通过为每个组注册一次，为每个事件使用许多不同的函数；或者通过使用 ``MGMT_EVT_OP_*_ALL`` 事件之一来为整个组启用所有通知；另外，处理程序还可以通过使用 :c:enumerator:`MGMT_EVT_OP_ALL` 为每个通知进行设置。设置处理程序时，只能组合属于同一组的事件；例如，可以通过一次注册调用设置 5 个 img_mgmt 回调，但如果还要为 os_mgmt 回调设置回调，则必须作为单独的注册来完成。组 ID 是数字递增的，事件 ID 是位掩码值，因此存在此限制。

例如，以下注册是允许的，它将在一次注册中使用单个回调函数注册 3 个 SMP 事件：

.. code-block:: c

    my_callback.callback = my_function;
    my_callback.event_id = (MGMT_EVT_OP_CMD_RECV |
                            MGMT_EVT_OP_CMD_STATUS |
                            MGMT_EVT_OP_CMD_DONE);
    mgmt_callback_register(&my_callback);

以下代码是不允许的，并且会导致未定义的操作，因为它将 IMG 管理组与 OS 管理组合在一起，而组 **不是** 位掩码值，只有事件才是：

.. code-block:: c

    my_callback.callback = my_function;
    my_callback.event_id = (MGMT_EVT_OP_IMG_MGMT_DFU_STARTED |
                            MGMT_EVT_OP_OS_MGMT_RESET);
    mgmt_callback_register(&my_callback);

.. _mcumgr_cb_events:

事件
====

可以通过启用相应 Kconfig 选项来选择事件：

 - :kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS`
    MCUmgr 命令状态（:c:enumerator:`MGMT_EVT_OP_CMD_RECV`、:c:enumerator:`MGMT_EVT_OP_CMD_STATUS`、:c:enumerator:`MGMT_EVT_OP_CMD_DONE`）
 - :kconfig:option:`CONFIG_MCUMGR_GRP_FS_FILE_ACCESS_HOOK`
    fs_mgmt 文件访问（:c:enumerator:`MGMT_EVT_OP_FS_MGMT_FILE_ACCESS`）
 - :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_UPLOAD_CHECK_HOOK`
    img_mgmt 上传检查（:c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CHUNK`）
 - :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_STATUS_HOOKS`
    img_mgmt 上传状态（:c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STOPPED`、:c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STARTED`、:c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_PENDING`、:c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CONFIRMED`）
 - :kconfig:option:`CONFIG_MCUMGR_GRP_OS_RESET_HOOK`
    os_mgmt 重置检查（:c:enumerator:`MGMT_EVT_OP_OS_MGMT_RESET`）
 - :kconfig:option:`CONFIG_MCUMGR_GRP_SETTINGS_ACCESS_HOOK`
    settings_mgmt 访问（:c:enumerator:`MGMT_EVT_OP_SETTINGS_MGMT_ACCESS`）

操作
====

某些回调期望返回状态以允许或禁止某项操作，例如 fs_mgmt 访问钩子，它允许允许或拒绝对文件的访问。对于这些处理程序，处理程序返回的第一个非 OK 错误码将返回给 MCUmgr 客户端。

选择性拒绝文件访问的示例：

.. code-block:: c

    #include <zephyr/kernel.h>
    #include <zephyr/mgmt/mcumgr/mgmt/mgmt.h>
    #include <zephyr/mgmt/mcumgr/mgmt/callbacks.h>
    #include <string.h>

    struct mgmt_callback my_callback;

    enum mgmt_cb_return my_function(uint32_t event, enum mgmt_cb_return prev_status,
                                    int32_t *rc, uint16_t *group, bool *abort_more,
                                    void *data, size_t data_size)
    {
        /* Only run this handler if a previous handler has not failed */
        if (event == MGMT_EVT_OP_FS_MGMT_FILE_ACCESS && prev_status == MGMT_CB_OK) {
            struct fs_mgmt_file_access *fs_data = (struct fs_mgmt_file_access *)data;

            /* Check if this is an upload and deny access if it is, otherwise check
             * the path and deny if is matches a name
             */
            if (fs_data->access == FS_MGMT_FILE_ACCESS_WRITE) {
                /* Return an access denied error code to the client and abort calling
                 * further handlers
                 */
                *abort_more = true;
                *rc = MGMT_ERR_EACCESSDENIED;

                return MGMT_CB_ERROR_RC;
            } else if (strcmp(fs_data->filename, "/lfs1/false_deny.txt") == 0) {
                /* Return a no entry error code to the client, call additional handlers
                 * (which will have failed set to true)
                 */
                *rc = MGMT_ERR_ENOENT;

                return MGMT_CB_ERROR_RC;
            }
        }

        /* Return OK status code to continue with acceptance to underlying handler */
        return MGMT_CB_OK;
    }

    int main()
    {
        my_callback.callback = my_function;
        my_callback.event_id = MGMT_EVT_OP_FS_MGMT_FILE_ACCESS;
        mgmt_callback_register(&my_callback);
    }

此代码为 :c:enumerator:`MGMT_EVT_OP_FS_MGMT_FILE_ACCESS` 事件注册一个处理程序，该处理程序将在收到 fs_mgmt 文件读/写命令后调用，以检查是否应允许对该文件的访问；请注意，这需要启用 :kconfig:option:`CONFIG_MCUMGR_GRP_FS_FILE_ACCESS_HOOK` 才能接收此回调。可以返回两类错误：可以将 ``rc`` 参数设置为 :c:enum:`mcumgr_err_t` 错误码并返回 :c:enumerator:`MGMT_CB_ERROR_RC`，或者可以将 ``group`` 值设置为组，将 ``rc`` 值设置为组错误码并返回 :c:enumerator:`MGMT_CB_ERROR_ERR`，从而设置组错误码（在 MCUmgr 协议版本 2 中引入）。

MCUmgr 命令回调用法/添加新事件类型
==================================

要为 MCUmgr 命令添加回调，可以使用事件 ID 调用 :c:func:`mgmt_callback_notify`，并可选地传入要传递给回调的数据结构（处理程序可以修改该结构）。如果不需要传回任何数据，可以改用 ``NULL``，并将数据大小设置为 0。

示例 MCUmgr 命令处理程序：

.. code-block:: c

    #include <zephyr/kernel.h>
    #include <zcbor_common.h>
    #include <zcbor_encode.h>
    #include <zephyr/mgmt/mcumgr/smp/smp.h>
    #include <zephyr/mgmt/mcumgr/mgmt/mgmt.h>
    #include <zephyr/mgmt/mcumgr/mgmt/callbacks.h>

    #define MGMT_EVT_GRP_USER_ONE MGMT_EVT_GRP_USER_CUSTOM_START

    enum user_one_group_events {
        /** Callback on first post, data is test_struct. */
        MGMT_EVT_OP_USER_ONE_FIRST  = MGMT_DEF_EVT_OP_ID(MGMT_EVT_GRP_USER_ONE, 0),

        /** Callback on second post, data is test_struct. */
        MGMT_EVT_OP_USER_ONE_SECOND = MGMT_DEF_EVT_OP_ID(MGMT_EVT_GRP_USER_ONE, 1),

        /** Used to enable all user_one events. */
        MGMT_EVT_OP_USER_ONE_ALL    = MGMT_DEF_EVT_OP_ALL(MGMT_EVT_GRP_USER_ONE),
    };

    struct test_struct {
        uint8_t some_value;
    };

    static int test_command(struct mgmt_ctxt *ctxt)
    {
        int rc;
        int err_rc;
        uint16_t err_group;
        zcbor_state_t *zse = ctxt->cnbe->zs;
        bool ok;
        struct test_struct test_data = {
            .some_value = 8,
        };

        rc = mgmt_callback_notify(MGMT_EVT_OP_USER_ONE_FIRST, &test_data,
                                  sizeof(test_data), &err_rc, &err_group);

        if (rc != MGMT_CB_OK) {
            /* A handler returned a failure code */
            if (rc == MGMT_CB_ERROR_RC) {
                /* The failure code is the RC value */
                return err_rc;
            }

            /* The failure is a group and ID error value */
            ok = smp_add_cmd_err(zse, err_group, (uint16_t)err_rc);
            goto end;
        }

        /* All handlers returned success codes */
        ok = zcbor_tstr_put_lit(zse, "output_value") &&
             zcbor_int32_put(zse, 1234);

    end:
        rc = (ok ? MGMT_ERR_EOK : MGMT_ERR_EMSGSIZE);

        return rc;
    }

如果回调不需要响应，可以调用该函数并将其强制转换为 void。

.. _mcumgr_cb_migration:

迁移
****

如果现有代码使用了 Zephyr 3.2 或更早版本中的旧回调系统，则需要将其迁移到新系统。要迁移代码，需要将以下回调注册函数改为使用 :c:func:`mgmt_callback_register` 注册回调（请注意，除了进行任何迁移外，还需要设置 :kconfig:option:`CONFIG_MCUMGR_MGMT_NOTIFICATION_HOOKS` 以启用新的通知系统）：

 * mgmt_evt
    使用 :c:enumerator:`MGMT_EVT_OP_CMD_RECV`、:c:enumerator:`MGMT_EVT_OP_CMD_STATUS` 或 :c:enumerator:`MGMT_EVT_OP_CMD_DONE` 作为同名事件的直接替代，其中提供的数据是 :c:struct:`mgmt_evt_op_cmd_arg`。需要设置 :kconfig:option:`CONFIG_MCUMGR_SMP_COMMAND_STATUS_HOOKS`。
 * fs_mgmt_register_evt_cb
    使用 :c:enumerator:`MGMT_EVT_OP_FS_MGMT_FILE_ACCESS`，其中提供的数据是 :c:struct:`fs_mgmt_file_access`。与返回 true 以允许操作或返回 false 以拒绝操作不同，需要返回 MCUmgr 结果码：:c:enumerator:`MGMT_ERR_EOK` 将允许该操作，任何其他返回码都将禁止该操作并将该码返回给客户端（访问被拒绝错误可以使用 :c:enumerator:`MGMT_ERR_EACCESSDENIED`）。需要设置 :kconfig:option:`CONFIG_MCUMGR_GRP_FS_FILE_ACCESS_HOOK`。
 * img_mgmt_register_callbacks
    如果使用了 ``dfu_started_cb``，则使用 :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STARTED`；如果使用了 ``dfu_stopped_cb``，则使用 :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_STOPPED`；如果使用了 ``dfu_pending_cb``，则使用 :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_PENDING`；如果使用了 ``dfu_confirmed_cb``，则使用 :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CONFIRMED`。这些回调没有任何返回状态。需要设置 :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_STATUS_HOOKS`。
 * img_mgmt_set_upload_cb
    使用 :c:enumerator:`MGMT_EVT_OP_IMG_MGMT_DFU_CHUNK`，其中提供的数据是 :c:struct:`img_mgmt_upload_check`。与返回 true 以允许操作或返回 false 以拒绝操作不同，需要返回 MCUmgr 结果码：:c:enumerator:`MGMT_ERR_EOK` 将允许该操作，任何其他返回码都将禁止该操作并将该码返回给客户端（访问被拒绝错误可以使用 :c:enumerator:`MGMT_ERR_EACCESSDENIED`）。需要设置 :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_UPLOAD_CHECK_HOOK`。
 * os_mgmt_register_reset_evt_cb
    使用 :c:enumerator:`MGMT_EVT_OP_OS_MGMT_RESET`。与返回 true 以允许操作或返回 false 以拒绝操作不同，需要返回 MCUmgr 结果码：:c:enumerator:`MGMT_ERR_EOK` 将允许该操作，任何其他返回码都将禁止该操作并将该码返回给客户端（访问被拒绝错误可以使用 :c:enumerator:`MGMT_ERR_EACCESSDENIED`）。需要设置 :kconfig:option:`CONFIG_MCUMGR_GRP_OS_RESET_HOOK`。

API 参考
********

.. doxygengroup:: mcumgr_callback_api
