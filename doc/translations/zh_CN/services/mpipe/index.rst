.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _mpipe:

多媒体流水线（mpipe）
#####################

.. contents::
   :local:
   :depth: 2

概述
****

多媒体流水线子系统（mpipe）用称为 **元素** 的自包含处理组件构建媒体流。应用声明所需的元素，将它们链接成图，并通过状态机驱动该图；mpipe 在相邻元素之间协商数据格式，确定由哪个缓冲区池提供缓冲区，并将这些缓冲区从一个元素移动到下一个元素。

.. graphviz::
   :align: center
   :caption: 流水线是由元素在其连接点处相连而成的图。

   digraph pipeline {
     rankdir=LR;
     node [shape=record, style=filled, fillcolor="#e8e8e8", fontname="sans"];
     edge [fontname="sans", fontsize=10];

     src   [label="{ source | { <o> src pad } }"];
     trans [label="{ { <i> sink pad } | transform | { <o> src pad } }"];
     sink  [label="{ { <i> sink pad } | sink }"];

     src:o   -> trans:i [label="negotiated format"];
     trans:o -> sink:i  [label="negotiated format"];
   }

mpipe 提供的是这些部件以及它们组合起来的规则，而不是现成的解决方案，因此组装流水线很像用乐高积木搭建：同一个图通过把它的元素绑定到不同设备，就能在另一块开发板上运行；而新的需求通常只是再添一个元素，而不是重写。

元素本身位于 **插件** 中，并按媒体域分组。插件自带目录、自己的 Kconfig 和自己的头文件，构建系统无需对框架做任何修改就能纳入它，因此芯片厂商或中间件提供商可以在不改动核心的情况下交付元素。

mpipe 不进行动态分配：缓冲区来自流水线启动时确定大小的池，协商路径上的一切都是固定大小并按值持有。开销转而落在栈上。协商在 :c:func:`mpipe_element_set_state` 内部运行，由调用它的那个线程执行，并同时持有多个活动的能力——需要在该线程上为此预留预算，对于下面的示例，就是运行 ``main`` 的那个线程。

mpipe 是可选的，而且它并不总是合适的工具。驱动单个设备的应用直接使用该设备的 API 会更好。只有当多个设备必须在格式上达成一致并相互传递缓冲区时，mpipe 才体现出自己的价值。

构建流水线
**********

对于整个核心 API，应用只需包含 ``<zephyr/mpipe/mpipe.h>``，而且只应包含它；它实例化的每个元素还会引入该元素自己的头文件。

元素是应用拥有的普通对象；mpipe 不分配其中任何一个。每种元素类型都有自己的初始化函数，该函数接受对应类型和一个 id：

.. code-block:: c

   /* Concrete element types come from plugins; each has its own header. */
   static struct mpipe pipe;
   static struct my_src source;
   static struct my_sink sink;

   ret = mpipe_pipeline_init(&pipe, PIPE_ID);
   ret = my_src_init(&source, SRC_ID);
   ret = my_sink_init(&sink, SINK_ID);

id 只需在流水线内唯一。元素通过属性来配置，这样调用者无需知道元素的具体类型就能对它进行设置：

.. code-block:: c

   ret = mpipe_object_set_properties((struct mpipe_object *)&source,
                                     MY_SRC_PROP_PATH, "/SD:/in.bin",
                                     MPIPE_PROP_LIST_END);

然后按任意顺序将它们添加到流水线中，并按流的顺序链接：

.. code-block:: c

   ret = mpipe_bin_add((struct mpipe_bin *)&pipe,
                       (struct mpipe_element *)&source,
                       (struct mpipe_element *)&sink, NULL);

   ret = mpipe_element_link((struct mpipe_element *)&source,
                            (struct mpipe_element *)&sink, NULL);

这些强制转换有明确含义，因为每个元素都把其基类作为第一个成员嵌入。链接时会拒绝能力不可能相交的一对元素，因此不可能成立的图会在构建时失败，而不是在启动时才失败。

将流水线设置为 ``MPIPE_STATE_PLAYING`` 并不是直接跳到该状态。流水线及其子元素按顺序逐步经过各个状态，从 ``READY`` 到 ``PAUSED`` 再到 ``PLAYING``，正因如此，格式才会在这个过程中被协商，各个池也会被启动。

随后应用会观察流水线的消息通道，既是为了了解运行如何结束，也是为了对失败采取行动。错误消息会指明引发它的元素以及当时所处的阶段，因此应用可以报告能力协商在第 3 个元素处失败，而不只是说明运行已停止。将图恢复为 ``MPIPE_STATE_READY`` 会将其拆除：

.. code-block:: c

   /* Needs CONFIG_ZBUS_MSG_SUBSCRIBER=y */
   ZBUS_MSG_SUBSCRIBER_DEFINE(main_sub);

   struct zbus_channel *bus = mpipe_element_get_bus_chan((struct mpipe_element *)&pipe);

   ret = zbus_chan_add_obs(bus, &main_sub, K_FOREVER);

   if (mpipe_element_set_state((struct mpipe_element *)&pipe, MPIPE_STATE_PLAYING) != 0) {
           /* the element that refused is still in its previous state */
   }

   do {
           ret = zbus_sub_wait_msg(&main_sub, &chan, &msg, K_FOREVER);
   } while ((msg.type & (MPIPE_MESSAGE_ERROR | MPIPE_MESSAGE_EOS)) == 0);

   (void)mpipe_element_set_state((struct mpipe_element *)&pipe, MPIPE_STATE_READY);

元素、连接点和链接
******************

每个 mpipe *元素* 都通过把 :c:struct:`mpipe_object` 作为第一个成员嵌入来从它派生。对象层承载了框架对其所持有的任何对象都需要的信息：一个 id、持有它的容器、链表链接以及属性回调。在此之上，:c:struct:`mpipe_element` 添加了状态机和连接点，各元素基类再对它进行特化。只承载数据的类型——能力、消息、分派——是不属于该层次结构的普通结构体：

.. graphviz::
   :align: center
   :caption: 继承就是结构体嵌入，因此向上转型就是普通的 C 强制转换。

   digraph inheritance {
     rankdir=BT;
     node [shape=box, style=filled, fillcolor="#e8e8e8", fontname="sans"];

     object    [label="mpipe_object", fillcolor="#d0d8e8"];
     element   [label="mpipe_element"];

     src       [label="mpipe_src"];
     sink      [label="mpipe_sink"];
     transform [label="mpipe_transform"];
     parser    [label="mpipe_parser"];
     bin       [label="mpipe_bin"];
     pipeline  [label="mpipe"];

     element -> object;
     src -> element;
     sink -> element;
     transform -> element;
     parser -> element;
     bin -> element;
     pipeline -> bin;

     subgraph cluster_data {
       label="plain data, outside the hierarchy";
       fontname="sans";
       style=dashed;
       color="#999999";
       node [style="filled,dashed", fillcolor="#f5f5f5"];
       structure [label="mpipe_structure"];
       value     [label="mpipe_value"];
       message   [label="mpipe_message"];
       dispatch  [label="mpipe_dispatch"];
     }
   }

* :c:struct:`mpipe_src` 产生缓冲区，并且只有源连接点。它还驱动协商，因为它位于图的头部。
* :c:struct:`mpipe_sink` 消费这些缓冲区，并且只有接收连接点。
* :c:struct:`mpipe_transform` 两者各有其一，并将输入转换为输出。
* :c:struct:`mpipe_parser` 将无固定形态的字节流切分成完整的帧，这与把一种格式转换为另一种格式是不同的工作。
* :c:struct:`mpipe_bin` 容纳其他元素，并按该转换所要求的顺序把状态变化转发给它们。
* :c:struct:`mpipe` 是顶层 bin：它拥有流线程和消息通道。

:c:struct:`mpipe_pad` 是两个元素交汇的地方。它带有一个方向（源或接收）、它所链接到的对端、在其上协商出的能力，以及框架分派到的回调：``chain_fn`` 接收缓冲区，``query_fn`` 回答查询，``event_fn`` 处理事件。链接两个元素就是把一个源连接点链接到一个接收连接点，流的每一跳都是这样一对连接。

状态机
******

元素处于三种状态之一，并在相邻状态之间一次移动一步：

.. graphviz::
   :align: center
   :caption: 每次转换的作用。

   digraph states {
     rankdir=LR;
     node [shape=box, style="rounded,filled", fillcolor="#e8e8e8", fontname="sans"];
     edge [fontname="sans", fontsize=10];

     READY -> PAUSED   [label=" negotiate the format,\l settle and start the pools\l"];
     PAUSED -> PLAYING [label=" start the source thread\l"];
     PLAYING -> PAUSED [label=" pause the source thread,\l keep what is queued\l"];
     PAUSED -> READY   [label=" flush, stop the pools,\l drop the negotiated formats\l"];
   }

``READY`` 表示已构建并已链接，不持有任何格式，也没有任何缓冲区。``READY`` 到 ``PAUSED`` 的转换才是实际工作发生的地方：源端驱动整个图上的能力协商，缓冲区池查询确定由谁提供缓冲区以及提供多少，随后各个池启动。

转换的方向决定了 bin 遍历其子元素的顺序：

* 向 **上** 转换时，子元素从接收端向源端转换，因此在有任何东西被推入下游元素之前，该元素就已就绪。
* 向 **下** 转换时，子元素从源端向接收端转换，因此不会有任何东西继续向一个已经拆除的元素产生数据。

失败的转换不会回退。拒绝转换的元素停留在原处，而已经移动的元素保持其新状态，这是有意为之的：由此得到的图恰好显示出是哪个元素在哪个转换中拒绝了。

能力协商
********

**能力** 描述跨越链接的数据：一种媒体类型加上一组字段，每个字段都是一个 :c:enum:`mpipe_caps_field` 标识符与一个 :c:struct:`mpipe_value` 的配对。它是一个 :c:struct:`mpipe_structure`，即按值持有的固定大小类型：

.. code-block:: c

   struct mpipe_structure s;

   mpipe_structure_init_fields(&s, MPIPE_MEDIA_VIDEO,
       MPIPE_CAPS_PIXEL_FORMAT, MPIPE_TYPE_UINT, VIDEO_PIX_FMT_RGB565,
       MPIPE_CAPS_IMAGE_WIDTH, MPIPE_TYPE_UINT_RANGE, 16, 1280, 2,
       MPIPE_CAPS_IMAGE_HEIGHT, MPIPE_TYPE_UINT_RANGE, 16, 720, 2,
       MPIPE_CAPS_END);

字段要么保存单个值，要么保存写成 ``[min, max, step]`` 的范围，因此上面的能力覆盖从 16 到 1280、步长为 2 的每一种宽度。当两个能力共享同一种媒体类型、至少有一个共同的字段标识符，并且每个共同字段的值都相交时，它们就相交。结果是两者的并集：共同字段保存相交后的值，而只有一侧携带的字段原样通过，这使得约束能够沿着一条本身并不关心该约束的元素链传递下去。*ANY* 能力不约束任何东西，并且与任何东西都相交——它是连接点在协商之前所携带的内容——而 *空* 能力不携带任何字段，也不与任何东西相交。

源端在 ``READY`` 到 ``PAUSED`` 时驱动协商，分两遍进行：

.. mermaid::
   :align: center
   :caption: 能力协商，由源端在 READY 到 PAUSED 时驱动
   :alt: Sequence diagram showing a caps query travelling from the source pad
       through the transform's two pads to the sink and the answer coming back,
       then the source fixating the format and a caps event travelling the same
       path while each element applies it with set_caps.

   %%{init: {'themeVariables': {'fontSize': '18px'}, 'sequence': {'actorFontSize': 18, 'messageFontSize': 18, 'noteFontSize': 18}}}%%
   sequenceDiagram
     autonumber
     participant so as src pad
     participant ti as sink pad
     participant to as src pad
     participant si as sink pad
     box rgba(79, 143, 214, 0.18) Source
     participant so
     end
     box rgba(148, 108, 196, 0.18) Transform
     participant ti
     participant to
     end
     box rgba(76, 168, 128, 0.18) Sink
     participant si
     end

     Note over so, si: Pass 1 - the caps query
     so ->> ti: can you take this format?
     ti ->> to: transform_caps()
     to ->> si: can you take this format?
     si -->> to: what I accept
     to ->> ti: transform_caps() back
     ti -->> so: what the chain accepts
     so ->> so: fixate to one format

     Note over so, si: Pass 2 - the caps event
     so ->> ti: this is the format
     ti ->> to: transform_caps(), narrowed
     to ->> si: this is the format
     si ->> si: set_caps()
     to ->> ti: set_caps() on both sides
     so ->> so: set_caps()

caps 查询向下游传播，每个元素先根据自己支持的内容对它进行收窄，再询问自己的下游，答案返回时已收窄为整条链的共有部分。如果某个元素拒绝，源端只是提供它支持的下一种格式，而不会让协商失败。

转换元素是最有意思的情况，因为它的两侧可能使用不同的格式：解码器输入一种格式，输出另一种格式。两侧并非必须不同——就地工作的元素会在缓冲区所在之处重写它，因此同一种格式会穿过该元素——但在确实不同的地方，``transform_caps`` 钩子负责把元素一侧的能力映射为另一侧随后可能成为的样子。查询在两个方向上都通过它穿过该元素：向外询问下游对端，返回时再以输入侧来表达答案。

答案中可能仍然带有范围，因此源端会 **固化** 它——把每个范围缩减为单个值——并把结果作为 caps 事件向下游通告。每个元素都通过自己的 ``set_caps`` 钩子应用其所在的一侧，硬件实际就是在这里配置的。

由于一个连接点持有的是单个能力而不是一组能力，支持多种格式的元素会按索引被逐一询问：框架先向它询问能力 0，再询问 1，依此类推，直到它报告没有更多为止。格式来自设备的元素通过询问其驱动来回答每个索引，因此不需要事先物化任何东西。

缓冲区池协商
************

仅凭格式并不能说明一个图需要多少缓冲区、它们必须多大、必须如何对齐，或者由谁的池来提供。紧接着格式固定之后，在同一次转换中，第二个查询会确定这些：

.. mermaid::
   :align: center
   :caption: 缓冲区池协商，紧接在格式固定之后
   :alt: Sequence diagram showing a buffer pool query travelling downstream to
       the sink, the sink proposing a pool or a config, and each element
       deciding and starting its own pool as the proposals come back upstream.

   %%{init: {'themeVariables': {'fontSize': '18px'}, 'sequence': {'actorFontSize': 18, 'messageFontSize': 18, 'noteFontSize': 18}}}%%
   sequenceDiagram
     autonumber
     participant so as src pad
     participant ti as sink pad
     participant to as src pad
     participant si as sink pad
     box rgba(79, 143, 214, 0.18) Source
     participant so
     end
     box rgba(148, 108, 196, 0.18) Transform
     participant ti
     participant to
     end
     box rgba(76, 168, 128, 0.18) Sink
     participant si
     end

     so ->> ti: buffer pool query
     ti ->> to: forwarded downstream first
     to ->> si: buffer pool query
     si -->> to: propose_buffer_pool()
     to ->> to: decide_buffer_pool(), start out_pool
     ti -->> so: propose_buffer_pool()
     so ->> so: decide_buffer_pool(), start pool

查询向下传播到接收端，提议则在返回途中写入，因此元素在做出任何决定之前，总是先拿到其下游的提议。

转换元素的两侧是独立确定的：``decide_buffer_pool`` 使用其下游提议的内容来敲定 **输出** 池，而 ``propose_buffer_pool`` 则用该元素在 **输入** 上所需的内容来回答上游查询。例外情况是直通，此时只有一个缓冲区穿过该元素，也只有一个池需要确定。

提议要么是整个池，要么是裸配置。提供池可让上游元素采用它并避免一次复制；提供配置则只陈述需求，而不移交任何东西。无论哪种方式，需求都只有通过 :c:func:`mpipe_buffer_pool_set_config` 才能到达其提议者仍然拥有的池，并由池的所有者对其进行校验、钳制或拒绝。

谁启动池，就由谁停止它，发生在 ``PAUSED`` 到 ``READY`` 时。正是这种对称性，让停止再重放的行为与首次运行一样。

缓冲区流动
**********

**缓冲区流动是零复制的。** 每个产生数据的元素都拥有一个 :c:struct:`mpipe_buffer_pool`，而池是在支撑它的任何东西之上的一组虚函数——``configure``、``set_config``、``start``、``stop``、``acquire_buffer``、``release_buffer``。正是这种间接性让插件可以交出驱动已经拥有的缓冲区，而不是它的副本，因此摄像头捕获的一帧画面可以送达显示器而无需被移动过。在元素之间传递的是引用，而不是像素。

缓冲区是 Zephyr 的 :c:struct:`net_buf` 分配，旁边还有一个 :c:struct:`mpipe_buffer_meta`，承载框架需要了解的关于单个缓冲区的信息：拥有它的池、其中有多少数据是有效的、一个时间戳。

:c:func:`mpipe_push_buffer` 会沿下游传递一个缓冲区：对于每一跳，它都会取出源连接点的对端，检查该连接点的刷新闸门，调用其 ``chain_fn``，然后沿着该元素产生的缓冲区走到下一个元素。NULL 输出表示缓冲区已被消费，遍历随即停止。链函数拥有交给它的缓冲区，即使在失败时也会释放它，因此所有权从不取决于所走的错误路径。

流水线运行时
************

流水线自己的线程驱动源端：它获取一个缓冲区并将其向下游推送，直到源端报告其数据结束，此时它会向下游发送一个流结束事件并暂停自身。需要把图的两半解耦到不同线程上的元素，通过在两者之间放置一个排队元素来实现。

拆除正在运行的图的顺序经过精心安排，正是这个顺序避免了数据丢失或死锁：

* ``PLAYING`` 到 ``PAUSED`` 只是暂停源端线程。已排队的内容都会保留，因此恢复时会继续而不会丢失。这是暂停，不是拆除。
* ``PAUSED`` 到 ``READY`` 会在子元素拆解各自的池 *之前* 在每个连接点上提起刷新闸门，因此仍在传输中的缓冲区会被丢弃，而不会被推入一个已经拆除的元素。只有在子元素排空 *之后* 才会等待流线程结束，因为如果某个子元素仍把该线程卡在满队列中，这个等待就会死锁。

消息通过流水线的消息通道传到应用，这是一个可用 :c:func:`mpipe_element_get_bus_chan` 访问的 zbus 通道。一条消息携带事情发生的位置——发出它的元素——以及发生的事情：一个类型，另外在失败时还有一个指出失败阶段的域和一个说明原因的 errno。它不携带面向人的字符串；描述失败的句子属于检测到该失败的站点的日志，而应用则根据域和 errno 进行分支。

具有多个接收端的流水线会为每个接收端产生一条流结束消息。流水线对它们进行计数，并且只传递最后一条，因此应用只会收到一次通知，也绝不会在某个分支仍在运行时拆除图。

编写元素
********

元素在框架之外编写，不需要对框架做任何改动。它把一个基类作为自己的第一个成员嵌入，用自身的 id 调用该基类的初始化函数，并只覆盖自己关心的内容：

.. code-block:: c

   struct my_sink {
           struct mpipe_sink sink;   /* must be first */
           const struct device *dev;
   };

   int my_sink_init(struct my_sink *self, uint8_t id)
   {
           int ret = mpipe_sink_init(&self->sink, id);

           if (ret != 0) {
                   return ret;
           }

           self->sink.sink_pad.enum_caps_fn = my_sink_enum_caps;
           self->sink.set_caps = my_sink_set_caps;

           return 0;
   }

重写 ``change_state`` 的元素必须链接到其基类，因为能力重置和池拆除——每个元素都应执行的操作——正是由基类完成的。

另一半工作是说明该元素支持什么。构建时已知的能力是一个 ``static const struct mpipe_structure``，元素从中复制；``MPIPE_STRUCTURE_DEFINE`` 会把其中一个放到 ``.rodata`` 中；有多个时则构成它们的数组。由设备支持的元素则改为在其 ``enum_caps_fn`` 内部通过询问驱动来构建每种能力，而由应用配置的元素则从属性中获取能力。

配置选项
********

* :kconfig:option:`CONFIG_MPIPE` 启用框架。每个插件都有自己的选项，并贡献自己的 Kconfig 文件。
* :kconfig:option:`CONFIG_MPIPE_STRUCTURE_MAX_FIELDS` 决定一个能力的大小。应按可能在一次相交中相遇的最大字段并集来确定它的大小，而不是按元素设置的字段数量，因为相交会携带只有一侧约束的字段。
* :kconfig:option:`CONFIG_MPIPE_NET_BUF_POOL_COUNT` 决定共享 ``net_buf`` 池的大小：即每条流水线在途缓冲区数量之和。
* :kconfig:option:`CONFIG_MPIPE_BIN_MAX_CHILDREN` 限制一个 bin 中的元素数量，它决定状态变化期间用于对元素排序的数组大小。
* :kconfig:option:`CONFIG_MPIPE_THREADS_NUM`、:kconfig:option:`CONFIG_MPIPE_THREAD_STACK_SIZE` 和 :kconfig:option:`CONFIG_MPIPE_THREAD_DEFAULT_PRIORITY` 配置流水线取用的池化线程。
* :kconfig:option:`CONFIG_MPIPE_WORKQUEUE` 让元素把有限的工作项卸载到共享的优先级工作队列上。
* :kconfig:option:`CONFIG_MPIPE_RPC` 构建在另一个核上运行其处理的客户端侧元素。
* :kconfig:option:`CONFIG_MPIPE_FAKE_SRC` 提供一个合成数据源，用于演练真实源需要硬件的图。

API 参考
********

.. doxygengroup:: mpipe_framework
