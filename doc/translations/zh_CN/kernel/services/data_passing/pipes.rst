.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _pipes_v2:

管道
####

:dfn:`管道` 是允许线程向另一个线程发送字节流的内核对象。管道支持高效的线程间通信，可以同步传输整个数据块或其中一部分。

.. contents::
    :local:
    :depth: 2

概念
****

可以定义任意数量的管道，仅受可用 RAM 限制。每个管道都通过其内存地址引用。

管道具有以下主要属性：

* **大小**，表示管道环形缓冲区的容量。大小为零表示该管道不带环形缓冲区。

管道必须初始化后才能使用。初始化后的管道为空。

线程按以下方式与管道交互：

- **写入**：线程以同步方式向管道写入全部或部分数据。接受的数据会直接复制给等待中的读取者，或复制到管道的环形缓冲区。如果环形缓冲区已满或没有环形缓冲区，操作会阻塞，直到有足够空间可用或指定的超时时间已到。

- **读取**：线程以同步方式从管道读取全部或部分数据。接受的数据来自管道的环形缓冲区，或直接从等待中的发送者复制。如果环形缓冲区为空或没有环形缓冲区，操作会阻塞，直到有数据可用或指定的超时时间已到。

- **重置**：线程可以重置管道，复位其内部状态，并使所有挂起的读写操作以错误码结束。

管道非常适合生产者—消费者模式、线程间流式数据传输等场景。

实现
****

管道使用 :c:struct:`k_pipe` 类型的变量和字节缓冲区定义，随后必须调用 :c:func:`k_pipe_init` 进行初始化。

以下代码定义并初始化一个空管道，其环形缓冲区可容纳 100 字节，并按 4 字节边界对齐：

.. code-block:: c

    uint8_t __aligned(4) my_ring_buffer[100];
    struct k_pipe my_pipe;

    k_pipe_init(&my_pipe, my_ring_buffer, sizeof(my_ring_buffer));

也可以使用 :c:macro:`K_PIPE_DEFINE` 宏在编译时定义并初始化管道，该宏同时定义管道及其环形缓冲区：

.. code-block:: c

    K_PIPE_DEFINE(my_pipe, 100, 4);

这与上面的代码效果相同。

不使用环形缓冲区时，缓冲区指针参数应为 NULL，大小参数应为 0。

写入管道
========

调用 :c:func:`k_pipe_write` 可以向管道添加数据。

以下示例展示如何使用管道将数据从生产者线程发送给一个或多个消费者线程。如果管道的环形缓冲区已满，生产者线程会等待指定的时间。

.. code-block:: c

   struct message_header {
       size_t num_data_bytes; /* Example field */
       ...
   };

   void producer_thread(void)
   {
       int rc;
       uint8_t *data;
       size_t total_size;
       size_t bytes_written;

       while (1) {
           /* Craft message to send in the pipe */
           make_message(data, &total_size);
           bytes_written = 0;

           /* Write data to the pipe, handling partial writes */
           while (bytes_written < total_size) {
               rc = k_pipe_write(&my_pipe, &data[bytes_written], total_size - bytes_written, K_NO_WAIT);

               if (rc < 0) {
                   /* Error occurred */
                   ...
                   break;
               } else {
                   /* Partial or full write succeeded; adjust for next iteration */
                   bytes_written += rc;
               }
           }

           /* Reset bytes_written for the next message */
           bytes_written = 0;
           ...
       }
   }

读取管道
========

调用 :c:func:`k_pipe_read` 可以从管道获取数据。

以下示例延续上面的生产者线程示例，展示一个处理生产者所生成数据的消费者线程。

.. code-block:: c

   struct message_header {
       size_t num_data_bytes; /* Example field */
       ...
   };

   void consumer_thread(void)
   {
       int rc;
       uint8_t buffer[128];
       size_t bytes_read = 0;
       struct message_header *header = (struct message_header *)buffer;

       while (1) {
           /* Step 1: Read the message header */
           bytes_read = 0;
      read_header:
           while (bytes_read < sizeof(*header)) {
               rc = k_pipe_read(&my_pipe, &buffer[bytes_read], sizeof(*header) - bytes_read, &bytes_read, K_NO_WAIT);

               if (rc < 0) {
                   /* Error occurred */
                   ...
                   goto read_header;
               }

               /* Adjust for partial reads */
               bytes_read += rc;
           }

           /* Step 2: Read the message body */
           bytes_read = 0;
           while (bytes_read < header->num_data_bytes) {
               rc = k_pipe_read(&my_pipe, &buffer[sizeof(*header) + bytes_read], header->num_data_bytes - bytes_read, K_NO_WAIT);

               if (rc < 0) {
                   /* Error occurred */
                   ...
                   goto read_header;
               }

               /* Adjust for partial reads */
               bytes_read += rc;
           }
           /* Successfully received the complete message */
       }
   }

重置管道
========

调用 :c:func:`k_pipe_reset` 可以重置管道。重置会复位管道的内部状态，并使所有挂起的操作以错误码结束。

以下示例展示如何在发生严重错误时重置管道：

.. code-block:: c

    void monitor_thread(void)
    {
        while (1) {
            ...
            /* Critical error detected: reset the entire pipe to reset it. */
            k_pipe_reset(&my_pipe);
            ...
        }
    }

使用建议
********

管道适用于在线程之间发送数据流。典型应用包括：

- 实现生产者—消费者模式。
- 在线程之间流式传输日志或数据包。
- 处理实时系统中的变长消息传递。

API 参考
********

.. doxygengroup:: pipe_apis
