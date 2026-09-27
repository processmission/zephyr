.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _settings_api:

设置
####

设置子系统为模块提供了一种存储每设备持久配置和运行时状态的方法。通过 FCB、NVS、ZMS 或文件系统，在通用 API 之后提供了多种存储实现。这些不同的实现让应用开发者可以灵活选择合适的存储介质，甚至可以在需求变化后更改存储介质。该子系统由各种 Zephyr 组件使用，也可以由用户应用同时使用。

设置项以键值对字符串形式存储。按照惯例，键可以按定义该键的包和子树来组织；例如，键 ``id/serial`` 将定义包 ``id`` 的 ``serial`` 配置元素。

提供了用于在键值与字符串类型之间进行转换的便捷例程。

有关设置子系统的示例，请参见 :zephyr:code-sample:`settings` 示例。

.. note::

   从 Zephyr 4.1 版本开始，推荐用于非文件系统存储的后端是 :ref:`NVS <nvs_api>` 和 :ref:`ZMS <zms_api>`。

处理程序
********

子树的设置处理程序实现一组处理函数。这些函数通过调用 :c:func:`settings_register()` 为动态处理程序注册，或通过调用 :c:macro:`SETTINGS_STATIC_HANDLER_DEFINE()` 为静态处理程序定义。

**h_get**
    当通过运行时后端使用 :c:func:`settings_runtime_get()` 按名称请求设置元素值时，会调用此函数。

**h_set**
    当使用 :c:func:`settings_load()` 从持久存储加载值，或从运行时后端使用 :c:func:`settings_runtime_set()` 时，会调用此函数。

**h_commit**
    在设置完全加载后会调用此函数。有时你不希望单个设置值立即生效，例如当有多个相互依赖的设置时。

**h_export**
    调用此函数以写入所有当前设置。当 :c:func:`settings_save()` 尝试保存设置或传输到任何用户实现的后端时，会发生这种情况。

设置处理程序还具有提交优先级 ``cprio``，可用于确定 ``h_commit`` 调用的优先级。例如，当某个子系统初始化其他 ``h_commit`` 调用所依赖的服务时，这可能是有利的。

设置处理程序的 ``h_commit`` 例程默认使用 ``cprio = 0`` 初始化；要以不同优先级初始化设置处理程序，可以对动态处理程序调用 :c:func:`settings_register_with_cprio()`，或对静态处理程序调用 :c:macro:`SETTINGS_STATIC_HANDLER_DEFINE_WITH_CPRIO()`。指定的 ``cprio`` 值是一个整数，值越小表示优先级越高。

后端
****

后端用于向设置处理程序加载数据或从中保存数据，并实现一组处理函数。对于可以加载数据的后端，通过调用 :c:func:`settings_src_register()` 注册；对于可以保存数据的后端，通过调用 :c:func:`settings_dst_register()` 注册。当前实现允许多个源后端，但只允许一个目标后端。

**csi_load**
    当使用 :c:func:`settings_load()` 从持久存储加载值时，会调用此函数。

**csi_load_one**
    当使用 :c:func:`settings_load_one()` 仅从持久存储加载一个项时，会调用此函数。

**csi_get_val_len**
    当使用 :c:func:`settings_get_val_len()` 从持久存储获取值的长度时，会调用此函数。

**csi_save**
    当使用 :c:func:`settings_save_one()` 将单个设置保存到持久存储时，会调用此函数。

**csi_save_start**
    当使用 :c:func:`settings_save()` 或 :c:func:`settings_save_subtree()` 开始保存所有当前设置时，会调用此函数。

**csi_save_end**
    在使用 :c:func:`settings_save()` 或 :c:func:`settings_save_subtree()` 保存所有当前设置之后，会调用此函数。

Zephyr 存储后端
***************

Zephyr 提供以下存储后端：

* Flash 循环缓冲区（:kconfig:option:`CONFIG_SETTINGS_FCB`）。
* 文件系统中的文件（:kconfig:option:`CONFIG_SETTINGS_FILE`）。
* 非易失性存储（:kconfig:option:`CONFIG_SETTINGS_NVS`）。
* Zephyr 内存存储（:kconfig:option:`CONFIG_SETTINGS_ZMS`）。

你可以为设置声明多个源；当调用 :c:func:`settings_load()` 时，所有这些源中的设置都会被恢复。

写入设置只能有一个目标；当你调用 :c:func:`settings_save()` 或 :c:func:`settings_save_one()` 时，数据就存储在该目标中。

FCB 读取目标使用 :c:func:`settings_fcb_src()` 注册，写入目标使用 :c:func:`settings_fcb_dst()` 注册。作为副作用，:c:func:`settings_fcb_src()` 会初始化 FCB 区域，因此必须在调用 :c:func:`settings_fcb_dst()` 之前调用它。文件读取目标使用 :c:func:`settings_file_src()` 注册，写入目标使用 :c:func:`settings_file_dst()` 注册。

非易失性存储读取目标使用 :c:func:`settings_nvs_src()` 注册，写入目标使用 :c:func:`settings_nvs_dst()` 注册。

Zephyr 内存存储（ZMS）读取目标使用 :c:func:`settings_zms_src()` 注册，写入目标使用 :c:func:`settings_zms_dst()` 注册。

ZMS 后端的特点是，在将设置键存储到持久存储之前，先使用哈希函数对其进行哈希处理。这种实现意味着，如果存储大量不同的键，键的哈希之间可能会发生一些冲突。该数量取决于所选的哈希函数。

ZMS 后端最多可以处理 :math:`2^n` 个冲突，其中 n 由（:kconfig:option:`CONFIG_SETTINGS_ZMS_MAX_COLLISIONS_BITS`）定义。


存储位置
********

默认情况下，FCB、非易失性存储（NVS）和 ZMS 后端会查找标签为“storage”的固定分区。可以通过设置 devicetree 中 chosen 节点的 ``zephyr,settings-partition`` 属性来选择不同的分区。

文件后端用于存储设置的文件路径通过 :kconfig:option:`CONFIG_SETTINGS_FILE_PATH` 选项选择。

从持久存储加载数据
******************

调用 :c:func:`settings_load()` 会使用 ``h_set`` 实现将设置数据从存储加载到易失性内存。加载所有数据后，会发出 ``h_commit`` 处理程序，通知应用设置已成功获取。

或者，调用 :c:func:`settings_load_one()` 只会加载一个设置条目，并将其存储在提供的缓冲区中。

可选地，为了仅获取与设置条目关联的值的长度，可以调用 :c:func:`settings_get_val_len()`。例如，动态分配数据缓冲区并需要在通过 settings_load_one() 读取数据之前获取数据大小的应用会使用此函数。

从技术上讲，FCB 和文件后端可能会存储实体的某些历史记录。这意味着最新的数据实体会存储在较早的现有数据实体之后。从 Zephyr 2.1 开始，后端必须过滤掉所有旧实体，并仅使用最新实体调用回调。

将数据存储到持久存储
********************

调用 :c:func:`settings_save_one()` 会使用后端实现将设置数据存储到存储介质。调用 :c:func:`settings_save()` 会使用 ``h_export`` 实现，通过 :c:func:`settings_save_one()` 在单个操作中存储不同的数据。只有打算由 :c:func:`settings_save()` 调用存储的键才需要由 ``h_export`` 覆盖。

对于 FCB 和文件后端，只会存储那些数据会改变键当前实际值的存储请求，因此无需检查应用是否更改了值。这种存储机制意味着存储中可以包含某个键的多个值赋值，而只有最后一个是该键的当前值。

垃圾回收
========
当存储已满（FCB）或占用过多空间（文件）时，后端会移除非最新的键值对记录和不必要的键删除记录。

安全域设置
**********
目前，设置不提供同一实例同时具备安全和非安全配置存储的方案。建议安全域使用自己的设置实例，并且如有需要（视情况而定），它可以使用专用接口为非安全域提供数据。

示例：设备配置
**************

这是一个简单示例，其中设置处理程序仅实现 ``h_set`` 和 ``h_export``。当从存储中恢复值（或在最初设置值时）会调用 ``h_set``，而 ``h_export`` 用于通过 ``storage_func()`` 将值写入存储。用户还可以实现其他导出功能（例如写入 shell 控制台）。

.. code-block:: c

    #define DEFAULT_FOO_VAL_VALUE 1

    static int8 foo_val = DEFAULT_FOO_VAL_VALUE;

    static int foo_settings_set(const char *name, size_t len,
                                settings_read_cb read_cb, void *cb_arg)
    {
        const char *next;
        int rc;

        if (settings_name_steq(name, "bar", &next) && !next) {
            if (len != sizeof(foo_val)) {
                return -EINVAL;
            }

            rc = read_cb(cb_arg, &foo_val, sizeof(foo_val));
            if (rc >= 0) {
                /* key-value pair was properly read.
                 * rc contains value length.
                 */
                return 0;
            }
            /* read-out error */
            return rc;
        }

        return -ENOENT;
    }

    static int foo_settings_export(int (*storage_func)(const char *name,
                                                       const void *value,
                                                       size_t val_len))
    {
        return storage_func("foo/bar", &foo_val, sizeof(foo_val));
    }

    struct settings_handler my_conf = {
        .name = "foo",
        .h_set = foo_settings_set,
        .h_export = foo_settings_export
    };

示例：持久化运行时状态
**********************

这是一个简单示例，展示如何持久化运行时状态。在此示例中，仅定义了 ``h_set``，用于从持久存储恢复值。

在此示例中，``main`` 函数递增 ``foo_val``，然后持久化最新数值。当系统重启时，应用会在初始化期间调用 :c:func:`settings_load()`，``foo_val`` 将从重启前的位置继续递增。

.. code-block:: c

    #include <zephyr/kernel.h>
    #include <zephyr/sys/reboot.h>
    #include <zephyr/settings/settings.h>
    #include <zephyr/sys/printk.h>
    #include <inttypes.h>

    #define DEFAULT_FOO_VAL_VALUE 0

    static uint8_t foo_val = DEFAULT_FOO_VAL_VALUE;

    static int foo_settings_set(const char *name, size_t len,
                                settings_read_cb read_cb, void *cb_arg)
    {
        const char *next;
        int rc;

        if (settings_name_steq(name, "bar", &next) && !next) {
            if (len != sizeof(foo_val)) {
                return -EINVAL;
            }

            rc = read_cb(cb_arg, &foo_val, sizeof(foo_val));
            if (rc >= 0) {
                return 0;
            }

            return rc;
        }


        return -ENOENT;
    }

    struct settings_handler my_conf = {
        .name = "foo",
        .h_set = foo_settings_set
    };

    int main(void)
    {
        settings_subsys_init();
        settings_register(&my_conf);
        settings_load();

        foo_val++;
        settings_save_one("foo/bar", &foo_val, sizeof(foo_val));

        printk("foo: %d\n", foo_val);

        k_msleep(1000);
        sys_reboot(SYS_REBOOT_COLD);
    }

示例：自定义后端实现
********************

这是一个简单示例，展示如何注册一个简单的自定义后端处理程序（:kconfig:option:`CONFIG_SETTINGS_CUSTOM`）。

.. code-block:: c

    static int settings_custom_load(struct settings_store *cs,
                                    const struct settings_load_arg *arg)
    {
        //...
    }

    static int settings_custom_save(struct settings_store *cs, const char *name,
                                    const char *value, size_t val_len)
    {
        //...
    }

    /* custom backend interface */
    static struct settings_store_itf settings_custom_itf = {
        .csi_load = settings_custom_load,
        .csi_save = settings_custom_save,
    };

    /* custom backend node */
    static struct settings_store settings_custom_store = {
        .cs_itf = &settings_custom_itf
    };

    int settings_backend_init(void)
    {
        /* register custom backend */
        settings_dst_register(&settings_custom_store);
        settings_src_register(&settings_custom_store);
        return 0;
    }

API 参考
********

设置子系统 API 由 :zephyr_file:`include/zephyr/settings/settings.h` 提供。

用于一般设置用法的 API
======================
.. doxygengroup:: settings

用于键名处理的 API
==================
.. doxygengroup:: settings_name_proc

用于运行时设置操作的 API
========================
.. doxygengroup:: settings_rt

后端接口的 API
==============
..  doxygengroup:: settings_backend
