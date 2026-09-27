.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _external_module_libmpix:

libmpix
#######

简介
****

`libmpix`_ 提供在微控制器上处理图像数据的库，支持像素格式转换、去拜耳化、模糊、锐化、颜色校正、缩放等操作。

它将多个操作串成流水线，省去中间缓冲区，使受限系统能在不牺牲性能的情况下处理更高分辨率的图像。

功能
****

* 简单的零复制流水线引擎，运行时开销低
* 减少内存开销，例如仅用 5 kB RAM 即可处理 1 MB 数据
* 支持 POSIX（Linux/BSD/macOS）和 Zephyr

在 Zephyr 中使用
****************

要将 libmpix 作为 Zephyr 模块引入，可以在 :file:`west.yaml` 中将其添加为 West 项目，也可以添加包含以下内容的子清单文件，例如 ``zephyr/submanifests/libmpix.yaml``，然后运行 :command:`west update`：

.. code-block:: yaml

   manifest:
     projects:
       - name: libmpix
         url: https://github.com/libmpix/libmpix.git
         revision: main
         path: modules/lib/libmpix

API 细节见 ``libmpix`` 头文件。下面给出一个简短示例。

.. code-block:: c

   #include <mpix/image.h>

   struct mpix_image img;

   mpix_image_from_buf(&img, buf_in, sizeof(buf_in), MPIX_FORMAT_RGB24);
   mpix_image_kernel(&img, MPIX_KERNEL_DENOISE, 5);
   mpix_image_kernel(&img, MPIX_KERNEL_SHARPEN, 3);
   mpix_image_convert(&img, MPIX_FORMAT_YUYV);
   mpix_image_to_buf(&img, buf_out, sizeof(buf_out));

   return img.err;

参考资料
********

.. target-notes::

.. _libmpix: https://github.com/libmpix/libmpix
