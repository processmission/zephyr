.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _semihost_guide:

半主机机制指南
##############

概述
****

半主机机制使运行在 ARM、RISC-V 和 Xtensa 目标上的代码能够与运行调试器或仿真器的主机通信，并使用主机的输入/输出功能。

有关可用功能的更完整文档，请参阅 `ARM Github documentation`_ 。

RISC-V 的功能借鉴了 ARM 的定义，详见 `RISC-V Github documentation`_ 。

Xtensa 上的半主机机制实现支持 GDB File-I/O 扩展，详见 `GDB File-I/O Remote Protocol`_ 。

文件操作
********

半主机机制允许应用打开、读取和修改主机上的文件。当需要使用超出仿真平台 ROM 容量的数据集来验证代码行为时，此功能很有用。文件路径可以是绝对路径，也可以是相对于运行进程所在目录的相对路径。

.. code-block:: c

   const char *path = "./data.bin";
   long file_len, bytes_read, fd;
   uint8_t buffer[16];

   /* Open the data file for reading */
   fd = semihost_open(path, SEMIHOST_OPEN_RB);
   if (fd < 0) {
      return -ENOENT;
   }
   /* Read all data from the file */
   file_len = semihost_flen(fd);
   while(file_len > 0) {
      bytes_read = semihost_read(fd, buffer, MIN(file_len, sizeof(buffer)));
      if (bytes_read < 0) {
         break;
      }
      /* Process read data */
      do_data_processing(buffer, bytes_read);
      /* Update remaining length */
      file_len -= bytes_read;
   }
   /* Close the file */
   semihost_close(fd);

附加功能
********

通过 :c:func:`semihost_exec` 直接执行 :c:enum:`semihost_instr` 中定义的半主机指令之一，可以使用附加功能。有关所需参数和返回码的完整文档，请参阅 `ARM Github documentation`_ 。

API 参考
********

.. doxygengroup:: semihost

.. _ARM Github documentation: https://github.com/ARM-software/abi-aa/blob/main/semihosting/semihosting.rst
.. _RISC-V Github documentation: https://github.com/riscv-non-isa/riscv-semihosting/blob/main/riscv-semihosting.adoc
.. _GDB File-I/O Remote Protocol: https://sourceware.org/gdb/current/onlinedocs/gdb.html/File_002dI_002fO-Remote-Protocol-Extension.html
