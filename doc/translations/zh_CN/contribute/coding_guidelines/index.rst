.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _coding_guidelines:

编码指南
########


Main rules
**********

编码指南规则基于 MISRA-C 2012，是 MISRA-C 的一个 **子集**。该子集在下表中列出，并附有规则摘要、其 MISRA-C 严重性以及来自其他标准的等效规则，供参考。

下表中的严重性和其他参考信息仅供参考。所列规则对 Zephyr 来说都是必需的，所有新代码都应遵守下面列出的规则。


.. note::

    对于现有的 Zephyr 维护者和协作者，如果你无法通过雇主获得一份副本，项目将提供数量有限的副本。如果你需要 MISRA-C 2012 的副本，请发送邮件至 safety@lists.zephyrproject.org，并详细说明你为何无法通过其他途径获得，以及拿到副本后预计会做出哪些贡献。安全委员会将审核所有申请。


.. list-table:: 主要规则
    :header-rows: 1
    :widths: 12 50 15 15

    * -  Zephyr 规则
      -  描述
      -  MISRA-C 2012 参考
      -  CERT C 参考

         .. _MisraC_Dir_1_1:
    * -  1
      -  程序输出所依赖的任何实现定义行为都应被记录并理解
      -  `Dir 1.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_01_01.c>`_
      -  | `FLP30-C <https://wiki.sei.cmu.edu/confluence/display/c/FLP30-C.+Do+not+use+floating-point+variables+as+loop+counters>`_
         | `MSC09-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC09-C.+Character+encoding%3A+Use+subset+of+ASCII+for+safety>`_
         | `EXP11-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP11-C.+Do+not+make+assumptions+regarding+the+layout+of+structures+with+bit-fields>`_

         .. _MisraC_Dir_2_1:
    * -  2
      -  所有源文件都应能在没有任何编译错误的情况下编译
      -  `Dir 2.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_02_01.c>`_
      -  不适用

         .. _MisraC_Dir_3_1:
    * -  3
      -  所有代码都应可追溯到已记录的需求
      -  `Dir 3.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_03_01.c>`_
      -  不适用

         .. _MisraC_Dir_4_1:
    * -  4
      -  应尽量减少运行期故障
      -  `Dir 4.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_01.c>`_
      -  不适用

         .. _MisraC_Dir_4_2:
    * -  5
      -  汇编语言的所有使用都应记录在案
      -  `Dir 4.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_02.c>`_
      -  不适用

         .. _MisraC_Dir_4_4:
    * -  6
      -  不应将代码段“注释掉”
      -  `Dir 4.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_04.c>`_
      -  `MSC04-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC04-C.+Use+comments+consistently+and+in+a+readable+fashion>`_

         .. _MisraC_Dir_4_5:
    * -  7
      -  同一命名空间中可见性重叠的标识符在排版上应无歧义
      -  `Dir 4.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_05.c>`_
      -  `DCL02-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL02-C.+Use+visually+distinct+identifiers>`_

         .. _MisraC_Dir_4_6:
    * -  8
      -  应使用表明大小和有符号性的 typedef 来替代基本数值类型
      -  `Dir 4.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_06.c>`_
      -  不适用

         .. _MisraC_Dir_4_7:
    * -  9
      -  如果函数返回错误信息，则应对该错误信息进行检验
      -  `Dir 4.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_07.c>`_
      -  不适用

         .. _MisraC_Dir_4_8:
    * -  10
      -  如果在某个翻译单元中从未解引用指向结构体或联合体的指针，则应隐藏该对象的实现
      -  | `Dir 4.8 example 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_08_1.c>`_
         | `Dir 4.8 example 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_08_2.c>`_
      -  `DCL12-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL12-C.+Implement+abstract+data+types+using+opaque+types>`_

         .. _MisraC_Dir_4_9:
    * -  11
      -  在函数与类函数宏可以互换使用时，应优先使用函数
      -  `Dir 4.9 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_09.c>`_
      -  `PRE00-C <https://wiki.sei.cmu.edu/confluence/display/c/PRE00-C.+Prefer+inline+or+static+functions+to+function-like+macros>`_

         .. _MisraC_Dir_4_10:
    * -  12
      -  应采取预防措施，防止头文件的内容被多次包含
      -  `Dir 4.10 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_10.c>`_
      -  `PRE06-C <https://wiki.sei.cmu.edu/confluence/display/c/PRE06-C.+Enclose+header+files+in+an+include+guard>`_

         .. _MisraC_Dir_4_11:
    * -  13
      -  应检查传递给库函数的值的有效性
      -  `Dir 4.11 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_11.c>`_
      -  不适用

         .. _MisraC_Dir_4_12:
    * - 14
      -  不得使用动态内存分配
      -  `Dir 4.12 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_12.c>`_
      -  | `API03-C <https://wiki.sei.cmu.edu/confluence/display/c/API03-C.+Create+consistent+interfaces+and+capabilities+across+related+functions>`_
         | `API04-C <https://wiki.sei.cmu.edu/confluence/display/c/API04-C.+Provide+a+consistent+and+usable+error-checking+mechanism>`_
         | `STR01-C <https://wiki.sei.cmu.edu/confluence/display/c/STR01-C.+Adopt+and+implement+a+consistent+plan+for+managing+strings>`_

         .. _MisraC_Dir_4_13:
    * -  15
      -  用于对资源执行操作的那些函数应按适当的顺序调用
      -  `Dir 4.13 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_13.c>`_
      -  不适用

         .. _MisraC_Dir_4_14:
    * -  16
      -  应检查从外部来源接收的值的有效性
      -  `Dir 4.14 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_14.c>`_
      -  不适用

         .. _MisraC_Rule_1_2:
    * -  17
      -  不应使用语言扩展
      -  `Rule 1.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_01_02.c>`_
      -  `MSC04-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC04-C.+Use+comments+consistently+and+in+a+readable+fashion>`_

         .. _MisraC_Rule_1_3:
    * -  18
      -  不得出现未定义行为或关键未指定行为
      -  `Rule 1.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_01_03.c>`_
      -  不适用

         .. _MisraC_Rule_2_1:
    * -  19
      -  项目中不得包含不可达代码
      -  | `Rule 2.1 example 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_02_01_1.c>`_
         | `Rule 2.1 example 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_02_01_2.c>`_
      -  `MSC12-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC12-C.+Detect+and+remove+code+that+has+no+effect+or+is+never+executed>`_

         .. _MisraC_Rule_2_2:
    * -  20
      -  不得存在死代码
      -  `Rule 2.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_02_02.c>`_
      -  | `DCL22-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL22-C.+Use+volatile+for+data+that+cannot+be+cached>`_
         | `MSC12-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC12-C.+Detect+and+remove+code+that+has+no+effect+or+is+never+executed>`_

         .. _MisraC_Rule_2_3:
    * -  21
      -  项目中不应包含未使用的类型声明
      -  `Rule 2.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_02_03.c>`_
      -  不适用

         .. _MisraC_Rule_2_6:
    * -  22
      -  函数中不应包含未使用的标签声明
      -  `Rule 2.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_02_06.c>`_
      -  不适用

         .. _MisraC_Rule_2_7:
    * -  23
      -  函数中不应有未使用的参数
      -  `Rule 2.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_02_07.c>`_
      -  不适用

         .. _MisraC_Rule_3_1:
    * -  24
      -  注释中不得出现字符序列 /* 和 //
      -  `Rule 3.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_03_01.c>`_
      -  `MSC04-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC04-C.+Use+comments+consistently+and+in+a+readable+fashion>`_

         .. _MisraC_Rule_3_2:
    * -  25
      -  // 注释中不得使用行拼接
      -  `Rule 3.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_03_02.c>`_
      -  不适用

         .. _MisraC_Rule_4_1:
    * -  26
      -  八进制和十六进制转义序列应正确终止
      -  `Rule 4.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_04_01.c>`_
      -  `MSC09-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC09-C.+Character+encoding%3A+Use+subset+of+ASCII+for+safety>`_

         .. _MisraC_Rule_4_2:
    * -  27
      -  不应使用三字符组
      -  `Rule 4.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_04_02.c>`_
      -  `PRE07-C <https://wiki.sei.cmu.edu/confluence/display/c/PRE07-C.+Avoid+using+repeated+question+marks>`_

         .. _MisraC_Rule_5_1:
    * -  28
      -  外部标识符应互不相同
      -  | `Rule 5.1 example 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_01_1.c>`_
         | `Rule 5.1 example 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_01_2.c>`_
      -  `DCL23-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL23-C.+Guarantee+that+mutually+visible+identifiers+are+unique>`_

         .. _MisraC_Rule_5_2:
    * -  29
      -  在同一作用域和命名空间中声明的标识符应互不相同
      -  `Rule 5.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_02.c>`_
      -  `DCL23-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL23-C.+Guarantee+that+mutually+visible+identifiers+are+unique>`_

         .. _MisraC_Rule_5_3:
    * -  30
      -  内层作用域中声明的标识符不得隐藏外层作用域中声明的标识符
      -  `Rule 5.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_03.c>`_
      -  | `DCL01-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL01-C.+Do+not+reuse+variable+names+in+subscopes>`_
         | `DCL23-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL23-C.+Guarantee+that+mutually+visible+identifiers+are+unique>`_

         .. _MisraC_Rule_5_4:
    * -  31
      -  宏标识符应互不相同
      -  `Rule 5.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_04.c>`_
      -  `DCL23-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL23-C.+Guarantee+that+mutually+visible+identifiers+are+unique>`_

         .. _MisraC_Rule_5_5:
    * -  32
      -  标识符应不同于宏名称
      -  `Rule 5.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_05.c>`_
      -  `DCL23-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL23-C.+Guarantee+that+mutually+visible+identifiers+are+unique>`_

         .. _MisraC_Rule_5_6:
    * -  33
      -  typedef 名称应是唯一的标识符
      -  `Rule 5.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_06.c>`_
      -  不适用

         .. _MisraC_Rule_5_7:
    * -  34
      -  标签名应是唯一的标识符
      -  `Rule 5.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_07.c>`_
      -  不适用

         .. _MisraC_Rule_5_8:
    * -  35
      -  定义具有外部链接的对象或函数的标识符应是唯一的
      -  | `Rule 5.8 example 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_08_1.c>`_
         | `Rule 5.8 example 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_08_2.c>`_
      -  不适用

         .. _MisraC_Rule_5_9:
    * -  36
      -  定义具有内部链接的对象或函数的标识符应是唯一的
      -  | `Rule 5.9 example 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_09_1.c>`_
         | `Rule 5.9 example 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_09_2.c>`_
      -  不适用

         .. _MisraC_Rule_6_1:
    * -  37
      -  位字段只能使用适当的类型声明
      -  `Rule 6.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_06_01.c>`_
      -  `INT14-C <https://wiki.sei.cmu.edu/confluence/display/c/INT14-C.+Avoid+performing+bitwise+and+arithmetic+operations+on+the+same+data>`_

         .. _MisraC_Rule_6_2:
    * -  38
      -  单比特的具名位字段不得为有符号类型
      -  `Rule 6.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_06_02.c>`_
      -  `INT14-C <https://wiki.sei.cmu.edu/confluence/display/c/INT14-C.+Avoid+performing+bitwise+and+arithmetic+operations+on+the+same+data>`_

         .. _MisraC_Rule_7_1:
    * -  39
      -  不得使用八进制常量
      -  `Rule 7.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_07_01.c>`_
      -  `DCL18-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL18-C.+Do+not+begin+integer+constants+with+0+when+specifying+a+decimal+value>`_

         .. _MisraC_Rule_7_2:
    * -  40
      -  对于以无符号类型表示的整型常量，都应加上 u 或 U 后缀
      -  `Rule 7.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_07_02.c>`_
      -  不适用

         .. _MisraC_Rule_7_3:
    * -  41
      -  字面量后缀中不得使用小写字符 l
      -  `Rule 7.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_07_03.c>`_
      -  `DCL16-C <https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152241>`_

         .. _MisraC_Rule_7_4:
    * -  42
      -  除非对象类型是指向 const 限定 char 的指针，否则不得将字符串字面量赋值给对象
      -  `Rule 7.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_07_04.c>`_
      -  不适用

         .. _MisraC_Rule_8_1:
    * -  43
      -  应显式指定类型
      -  `Rule 8.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_01.c>`_
      -  `DCL31-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL31-C.+Declare+identifiers+before+using+them>`_

         .. _MisraC_Rule_8_2:
    * -  44
      -  函数类型应采用带具名参数的原型形式
      -  `Rule 8.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_02.c>`_
      -  | `DCL07-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL07-C.+Include+the+appropriate+type+information+in+function+declarators>`_
         | `DCL20-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL20-C.+Explicitly+specify+void+when+a+function+accepts+no+arguments>`_
         | `DCL36-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL36-C.+Do+not+declare+an+identifier+with+conflicting+linkage+classifications>`_
         | `EXP37-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP37-C.+Call+functions+with+the+correct+number+and+type+of+arguments>`_

         .. _MisraC_Rule_8_3:
    * -  45
      -  对象或函数的所有声明都应使用相同的名称和类型限定符
      -  `Rule 8.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_03.c>`_
      -  不适用

         .. _MisraC_Rule_8_4:
    * -  46
      -  定义具有外部链接的对象或函数时，应有兼容的声明可见
      -  `Rule 8.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_04.c>`_
      -  | `DCL36-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL36-C.+Do+not+declare+an+identifier+with+conflicting+linkage+classifications>`_
         | `DCL40-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL40-C.+Do+not+create+incompatible+declarations+of+the+same+function+or+object>`_

         .. _MisraC_Rule_8_5:
    * -  47
      -  外部对象或函数应仅在一个文件中声明一次
      -  | `Rule 8.5 example 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_05_1.c>`_
         | `Rule 8.5 example 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_05_2.c>`_
      -  不适用

         .. _MisraC_Rule_8_6:
    * -  48
      -  具有外部链接的标识符应恰好有一个外部定义
      -  | `Rule 8.6 example 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_06_1.c>`_
         | `Rule 8.6 example 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_06_2.c>`_
      -  不适用

         .. _MisraC_Rule_8_8:
    * -  49
      -  具有内部链接的对象和函数的所有声明都应使用 static 存储类说明符
      -  `Rule 8.8 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_08.c>`_
      -  | `DCL15-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL15-C.+Declare+file-scope+objects+or+functions+that+do+not+need+external+linkage+as+static>`_
         | `DCL36-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL36-C.+Do+not+declare+an+identifier+with+conflicting+linkage+classifications>`_

         .. _MisraC_Rule_8_9:
    * -  50
      -  如果对象的标识符只出现在单个函数中，则该对象宜在块作用域中定义
      -  `Rule 8.9 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_09.c>`_
      -  `DCL19-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL19-C.+Minimize+the+scope+of+variables+and+functions>`_

         .. _MisraC_Rule_8_10:
    * -  51
      -  内联函数应使用 static 存储类声明
      -  `Rule 8.10 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_10.c>`_
      -  不适用

         .. _MisraC_Rule_8_12:
    * -  52
      -  在枚举项列表中，隐式指定的枚举常量的值应是唯一的
      -  `Rule 8.12 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_12.c>`_
      -  `INT09-C <https://wiki.sei.cmu.edu/confluence/display/c/INT09-C.+Ensure+enumeration+constants+map+to+unique+values>`_

         .. _MisraC_Rule_8_14:
    * -  53
      -  不得使用 restrict 类型限定符
      -  `Rule 8.14 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_14.c>`_
      -  `EXP43-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP43-C.+Avoid+undefined+behavior+when+using+restrict-qualified+pointers>`_

         .. _MisraC_Rule_9_1:
    * -  54
      -  不得在设置具有自动存储期的对象的值之前读取它
      -  `Rule 9.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_09_01.c>`_
      -  不适用

         .. _MisraC_Rule_9_2:
    * -  55
      -  聚合或联合体的初始化器应使用花括号括起
      -  `Rule 9.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_09_02.c>`_
      -  不适用

         .. _MisraC_Rule_9_3:
    * -  56
      -  不得对数组进行部分初始化
      -  `Rule 9.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_09_03.c>`_
      -  不适用

         .. _MisraC_Rule_9_4:
    * -  57
      -  对象的某个元素不得被初始化多次
      -  `Rule 9.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_09_04.c>`_
      -  不适用

         .. _MisraC_Rule_9_5:
    * -  58
      -  使用指定初始化器初始化数组对象时，应显式指定数组大小
      -  `Rule 9.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_09_05.c>`_
      -  `ARR02-C <https://wiki.sei.cmu.edu/confluence/display/c/ARR02-C.+Explicitly+specify+array+bounds%2C+even+if+implicitly+defined+by+an+initializer>`_

         .. _MisraC_Rule_10_1:
    * -  59
      -  操作数不得具有不恰当的本质类型
      -  `Rule 10.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_10_01.c>`_
      -  | `INT02-C <https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules>`_
         | `INT07-C <https://wiki.sei.cmu.edu/confluence/display/c/INT07-C.+Use+only+explicitly+signed+or+unsigned+char+type+for+numeric+values>`_
         | `INT12-C <https://wiki.sei.cmu.edu/confluence/display/c/INT12-C.+Do+not+make+assumptions+about+the+type+of+a+plain+int+bit-field+when+used+in+an+expression>`_
         | `INT31-C <https://wiki.sei.cmu.edu/confluence/display/c/INT31-C.+Ensure+that+integer+conversions+do+not+result+in+lost+or+misinterpreted+data>`_
         | `STR04-C <https://wiki.sei.cmu.edu/confluence/display/c/STR04-C.+Use+plain+char+for+characters+in+the+basic+character+set>`_
         | `STR34-C <https://wiki.sei.cmu.edu/confluence/display/c/STR34-C.+Cast+characters+to+unsigned+char+before+converting+to+larger+integer+sizes>`_

         .. _MisraC_Rule_10_2:
    * -  60
      -  本质为字符类型的表达式不得被不恰当地用于加法和减法运算
      -  `Rule 10.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_10_02.c>`_
      -  | `STR04-C <https://wiki.sei.cmu.edu/confluence/display/c/STR04-C.+Use+plain+char+for+characters+in+the+basic+character+set>`_
         | `STR34-C <https://wiki.sei.cmu.edu/confluence/display/c/STR34-C.+Cast+characters+to+unsigned+char+before+converting+to+larger+integer+sizes>`_

         .. _MisraC_Rule_10_3:
    * -  61
      -  不得将表达式的值赋给本质类型更窄或本质类型类别不同的对象
      -  `Rule 10.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_10_03.c>`_
      -  | `INT02-C <https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules>`_
         | `INT07-C <https://wiki.sei.cmu.edu/confluence/display/c/INT07-C.+Use+only+explicitly+signed+or+unsigned+char+type+for+numeric+values>`_
         | `INT31-C <https://wiki.sei.cmu.edu/confluence/display/c/INT31-C.+Ensure+that+integer+conversions+do+not+result+in+lost+or+misinterpreted+data>`_
         | `STR04-C <https://wiki.sei.cmu.edu/confluence/display/c/STR04-C.+Use+plain+char+for+characters+in+the+basic+character+set>`_
         | `STR34-C <https://wiki.sei.cmu.edu/confluence/display/c/STR34-C.+Cast+characters+to+unsigned+char+before+converting+to+larger+integer+sizes>`_

         .. _MisraC_Rule_10_4:
    * -  62
      -  对于会执行通常算术转换的运算符，其两个操作数应具有相同的本质类型类别
      -  `Rule 10.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_10_04.c>`_
      -  | `INT02-C <https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules>`_
         | `INT07-C <https://wiki.sei.cmu.edu/confluence/display/c/INT07-C.+Use+only+explicitly+signed+or+unsigned+char+type+for+numeric+values>`_
         | `INT31-C <https://wiki.sei.cmu.edu/confluence/display/c/INT31-C.+Ensure+that+integer+conversions+do+not+result+in+lost+or+misinterpreted+data>`_
         | `STR04-C <https://wiki.sei.cmu.edu/confluence/display/c/STR04-C.+Use+plain+char+for+characters+in+the+basic+character+set>`_
         | `STR34-C <https://wiki.sei.cmu.edu/confluence/display/c/STR34-C.+Cast+characters+to+unsigned+char+before+converting+to+larger+integer+sizes>`_

         .. _MisraC_Rule_10_5:
    * -  63
      -  不应将表达式的值转换为不恰当的本质类型
      -  `Rule 10.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_10_05.c>`_
      -  | `EXP14-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP14-C.+Beware+of+integer+promotion+when+performing+bitwise+operations+on+integer+types+smaller+than+int>`_
         | `INT02-C <https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules>`_

         .. _MisraC_Rule_10_6:
    * -  64
      -  不得将复合表达式的值赋给本质类型更宽的对象
      -  `Rule 10.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_10_06.c>`_
      -  | `INT02-C <https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules>`_
         | `INT31-C <https://wiki.sei.cmu.edu/confluence/display/c/INT31-C.+Ensure+that+integer+conversions+do+not+result+in+lost+or+misinterpreted+data>`_

         .. _MisraC_Rule_10_7:
    * -  65
      -  如果将复合表达式用作会执行通常算术转换的运算符的一个操作数，则另一个操作数不得具有更宽的本质类型
      -  `Rule 10.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_10_07.c>`_
      -  | `INT02-C <https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules>`_
         | `INT31-C <https://wiki.sei.cmu.edu/confluence/display/c/INT31-C.+Ensure+that+integer+conversions+do+not+result+in+lost+or+misinterpreted+data>`_

         .. _MisraC_Rule_10_8:
    * -  66
      -  不得将复合表达式的值转换为不同的本质类型类别或更宽的本质类型
      -  `Rule 10.8 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_10_08.c>`_
      -  `INT02-C <https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules>`_

         .. _MisraC_Rule_11_2:
    * -  67
      -  不得在不完整类型的指针与其他任何类型之间进行转换
      -  `Rule 11.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_11_02.c>`_
      -  `EXP36-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP36-C.+Do+not+cast+pointers+into+more+strictly+aligned+pointer+types>`_

         .. _MisraC_Rule_11_6:
    * -  68
      -  不得在指向 void 的指针与算术类型之间进行强制转换
      -  `Rule 11.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_11_06.c>`_
      -  不适用

         .. _MisraC_Rule_11_7:
    * -  69
      -  不得在指向对象的指针与非整数算术类型之间进行强制转换
      -  `Rule 11.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_11_07.c>`_
      -  `EXP36-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP36-C.+Do+not+cast+pointers+into+more+strictly+aligned+pointer+types>`_

         .. _MisraC_Rule_11_8:
    * -  70
      -  强制转换不得移除指针所指向类型的任何 const 或 volatile 限定
      -  `Rule 11.8 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_11_08.c>`_
      -  | `EXP05-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP05-C.+Do+not+cast+away+a+const+qualification>`_
         | `EXP32-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP32-C.+Do+not+access+a+volatile+object+through+a+nonvolatile+reference>`_

         .. _MisraC_Rule_11_9:
    * -  71
      -  宏 NULL 应是唯一允许的整数空指针常量形式
      -  `Rule 11.9 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_11_09.c>`_
      -  不适用

         .. _MisraC_Rule_12_1:
    * -  72
      -  表达式中运算符的优先级宜显式化
      -  `Rule 12.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_12_01.c>`_
      -  `EXP00-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP00-C.+Use+parentheses+for+precedence+of+operation>`_

         .. _MisraC_Rule_12_2:
    * -  73
      -  移位运算符的右操作数应位于 0 到左操作数本质类型位宽减一的范围之内
      -  `Rule 12.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_12_02.c>`_
      -  不适用

         .. _MisraC_Rule_12_4:
    * -  74
      -  常量表达式的求值不应导致无符号整数回绕
      -  `Rule 12.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_12_04.c>`_
      -  不适用

         .. _MisraC_Rule_12_5:
    * -  75
      -  sizeof 运算符的操作数不得是声明为“类型数组”的函数参数
      -  `Rule 12.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_12_05.c>`_
      -  不适用

         .. _MisraC_Rule_13_1:
    * -  76
      -  初始化列表中不得包含持久性副作用
      -  | `Rule 13.1 example 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_13_01_1.c>`_
         | `Rule 13.1 example 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_13_01_2.c>`_
      -  不适用

         .. _MisraC_Rule_13_2:
    * -  77
      -  在所有允许的求值顺序下，表达式的值及其持久性副作用都应相同
      -  `Rule 13.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_13_02.c>`_
      -  `EXP30-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP30-C.+Do+not+depend+on+the+order+of+evaluation+for+side+effects>`_

         .. _MisraC_Rule_13_3:
    * -  78
      -  包含自增（++）或自减（--）运算符的完整表达式，除该自增或自减运算符引起的副作用外，不应有其他潜在副作用
      -  `Rule 13.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_13_03.c>`_
      -  不适用

         .. _MisraC_Rule_13_4:
    * -  79
      -  不应使用赋值运算符的结果
      -  `Rule 13.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_13_04.c>`_
      -  不适用

         .. _MisraC_Rule_13_5:
    * -  80
      -  逻辑 && 或 || 运算符的右操作数不得包含持久性副作用
      -  | `Rule 13.5 example 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_13_05_1.c>`_
         | `Rule 13.5 example 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_13_05_2.c>`_
      -  `EXP10-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP10-C.+Do+not+depend+on+the+order+of+evaluation+of+subexpressions+or+the+order+in+which+side+effects+take+place>`_

         .. _MisraC_Rule_13_6:
    * -  81
      -  sizeof 运算符的操作数不得包含任何具有潜在副作用的表达式
      -  `Rule 13.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_13_06.c>`_
      -  不适用

         .. _MisraC_Rule_14_1:
    * -  82
      -  循环计数器不得具有本质浮点类型
      -  `Rule 14.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_14_01.c>`_
      -  `FLP30-C <https://wiki.sei.cmu.edu/confluence/display/c/FLP30-C.+Do+not+use+floating-point+variables+as+loop+counters>`_

         .. _MisraC_Rule_14_2:
    * -  83
      -  for 循环应是良构的
      -  `Rule 14.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_14_02.c>`_
      -  不适用

         .. _MisraC_Rule_14_3:
    * -  84
      -  控制表达式不得是不变的
      -  `Rule 14.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_14_03.c>`_
      -  不适用

         .. _MisraC_Rule_14_4:
    * -  85
      -  if 语句的控制表达式和迭代语句的控制表达式应具有本质布尔类型
      -  `Rule 14.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_14_04.c>`_
      -  不适用

         .. _MisraC_Rule_15_2:
    * -  86
      -  goto 语句应跳转到同一函数中在其之后声明的标签
      -  `Rule 15.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_15_02.c>`_
      -  不适用

         .. _MisraC_Rule_15_3:
    * -  87
      -  goto 语句引用的任何标签都应声明在同一块中，或声明在包含该 goto 语句的任何块中
      -  `Rule 15.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_15_03.c>`_
      -  不适用

         .. _MisraC_Rule_15_6:
    * -  88
      -  迭代语句或选择语句的语句体应是复合语句
      -  `Rule 15.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_15_06.c>`_
      -  `EXP19-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP19-C.+Use+braces+for+the+body+of+an+if%2C+for%2C+or+while+statement>`_

         .. _MisraC_Rule_15_7:
    * -  89
      -  所有 if else if 构造都应以 else 语句结束
      -  `Rule 15.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_15_07.c>`_
      -  `MSC01-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC01-C.+Strive+for+logical+completeness>`_

         .. _MisraC_Rule_16_1:
    * -  90
      -  所有 switch 语句都应是良构的
      -  `Rule 16.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_16_01.c>`_
      -  `DCL41-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL41-C.+Do+not+declare+variables+inside+a+switch+statement+before+the+first+case+label>`_

         .. _MisraC_Rule_16_2:
    * -  91
      -  只有当最内层包围的复合语句是 switch 语句的语句体时，才可使用 switch 标签
      -  `Rule 16.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_16_02.c>`_
      -  `MSC20-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC20-C.+Do+not+use+a+switch+statement+to+transfer+control+into+a+complex+block>`_

         .. _MisraC_Rule_16_3:
    * -  92
      -  每个 switch 分支都应以无条件的 break 语句结束
      -  `Rule 16.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_16_03.c>`_
      -  不适用

         .. _MisraC_Rule_16_4:
    * -  93
      -  每个 switch 语句都应有 default 标签
      -  `Rule 16.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_16_04.c>`_
      -  不适用

         .. _MisraC_Rule_16_5:
    * -  94
      -  default 标签应作为 switch 语句的第一个或最后一个 switch 标签出现
      -  `Rule 16.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_16_05.c>`_
      -  不适用

         .. _MisraC_Rule_16_6:
    * -  95
      -  每个 switch 语句都应至少有两个 switch 分支
      -  `Rule 16.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_16_06.c>`_
      -  不适用

         .. _MisraC_Rule_16_7:
    * -  96
      -  switch 表达式不得具有本质布尔类型
      -  `Rule 16.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_16_07.c>`_
      -  不适用

         .. _MisraC_Rule_17_1:
    * -  97
      -  不得使用 <stdarg.h> 的功能
      -  `Rule 17.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_17_01.c>`_
      -  | `DCL10-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL10-C.+Maintain+the+contract+between+the+writer+and+caller+of+variadic+functions>`_
         | `DCL11-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL11-C.+Understand+the+type+issues+associated+with+variadic+functions>`_
         | `ERR00-C <https://wiki.sei.cmu.edu/confluence/display/c/ERR00-C.+Adopt+and+implement+a+consistent+and+comprehensive+error-handling+policy>`_

         .. _MisraC_Rule_17_2:
    * -  98
      -  函数不得直接或间接调用自身
      -  `Rule 17.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_17_02.c>`_
      -  `MEM05-C <https://wiki.sei.cmu.edu/confluence/display/c/MEM05-C.+Avoid+large+stack+allocations>`_

         .. _MisraC_Rule_17_3:
    * -  99
      -  不得隐式声明函数
      -  `Rule 17.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_17_03.c>`_
      -  | `DCL36-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL36-C.+Do+not+declare+an+identifier+with+conflicting+linkage+classifications>`_
         | `EXP37-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP37-C.+Call+functions+with+the+correct+number+and+type+of+arguments>`_

         .. _MisraC_Rule_17_4:
    * -  100
      -  返回类型非 void 的函数的所有退出路径都应有一个带表达式的显式 return 语句
      -  `Rule 17.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_17_04.c>`_
      -  不适用

         .. _MisraC_Rule_17_5:
    * -  101
      -  对应于声明为数组类型的参数的函数实参，应具有适当数量的元素
      -  `Rule 17.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_17_05.c>`_
      -  不适用

         .. _MisraC_Rule_17_6:
    * -  102
      -  数组参数的声明中不得在 [ ] 之间包含 static 关键字
      -  `Rule 17.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_17_06.c>`_
      -  不适用

         .. _MisraC_Rule_17_7:
    * -  103
      -  应使用返回类型非 void 的函数所返回的值
      -  `Rule 17.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_17_07.c>`_
      -  不适用

         .. _MisraC_Rule_18_1:
    * -  104
      -  对指针操作数进行算术运算所得的指针，应指向与该指针操作数相同的数组中的元素
      -  `Rule 18.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_18_01.c>`_
      -  | `ARR30-C <https://wiki.sei.cmu.edu/confluence/display/c/ARR30-C.+Do+not+form+or+use+out-of-bounds+pointers+or+array+subscripts>`_
         | `ARR39-C <https://wiki.sei.cmu.edu/confluence/display/c/ARR39-C.+Do+not+add+or+subtract+a+scaled+integer+to+a+pointer>`_
         | `EXP08-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP08-C.+Ensure+pointer+arithmetic+is+used+correctly>`_

         .. _MisraC_Rule_18_2:
    * -  105
      -  指针之间的减法只应应用于指向同一数组中元素的指针
      -  `Rule 18.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_18_02.c>`_
      -  | `ARR39-C <https://wiki.sei.cmu.edu/confluence/display/c/ARR39-C.+Do+not+add+or+subtract+a+scaled+integer+to+a+pointer>`_
         | `EXP08-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP08-C.+Ensure+pointer+arithmetic+is+used+correctly>`_

         .. _MisraC_Rule_18_3:
    * -  106
      -  关系运算符 >、>=、< 和 <= 不得应用于指针类型的对象，除非它们指向同一对象内部
      -  `Rule 18.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_18_03.c>`_
      -  | `ARR39-C <https://wiki.sei.cmu.edu/confluence/display/c/ARR39-C.+Do+not+add+or+subtract+a+scaled+integer+to+a+pointer>`_
         | `EXP08-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP08-C.+Ensure+pointer+arithmetic+is+used+correctly>`_

         .. _MisraC_Rule_18_5:
    * -  107
      -  声明中的指针嵌套层级不应超过两级
      -  `Rule 18.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_18_05.c>`_
      -  不适用

         .. _MisraC_Rule_18_6:
    * -  108
      -  不得将具有自动存储期的对象的地址复制到在第一个对象失效之后仍然存在的另一个对象中
      -  | `Rule 18.6 example 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_18_06_1.c>`_
         | `Rule 18.6 example 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_18_06_2.c>`_
      -  | `DCL30-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL30-C.+Declare+objects+with+appropriate+storage+durations>`_
         | `MEM30-C <https://wiki.sei.cmu.edu/confluence/display/c/MEM30-C.+Do+not+access+freed+memory>`_

         .. _MisraC_Rule_18_8:
    * -  109
      -  不得使用变长数组类型
      -  `Rule 18.8 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_18_08.c>`_
      -  不适用

         .. _MisraC_Rule_19_1:
    * -  110
      -  不得将对象赋值或复制到与其重叠的对象
      -  `Rule 19.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_19_01.c>`_
      -  不适用

         .. _MisraC_Rule_20_2:
    * -  111
      -  字符 '、\ 以及字符序列 /* 或 // 不得出现在头文件名中
      -  `Rule 20.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_02.c>`_
      -  不适用

         .. _MisraC_Rule_20_3:
    * -  112
      -  #include 指令后面应跟随 <filename> 或 “filename” 序列
      -  `Rule 20.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_03.c>`_
      -  不适用

         .. _MisraC_Rule_20_4:
    * -  113
      -  不得定义与关键字同名的宏
      -  `Rule 20.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_04.c>`_
      -  不适用

         .. _MisraC_Rule_20_7:
    * -  114
      -  由宏参数展开得到的表达式应使用圆括号括起
      -  `Rule 20.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_07.c>`_
      -  `PRE01-C <https://wiki.sei.cmu.edu/confluence/display/c/PRE01-C.+Use+parentheses+within+macros+around+parameter+names>`_

         .. _MisraC_Rule_20_8:
    * -  115
      -  #if 或 #elif 预处理指令的控制表达式的求值结果应为 0 或 1
      -  `Rule 20.8 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_08.c>`_
      -  不适用

         .. _MisraC_Rule_20_9:
    * -  116
      -  #if 或 #elif 预处理指令的控制表达式中使用的所有标识符都应在求值前用 #define 定义
      -  `Rule 20.9 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_09.c>`_
      -  不适用

         .. _MisraC_Rule_20_11:
    * -  117
      -  紧跟在 # 运算符之后的宏参数，其后不得紧跟 ## 运算符
      -  `Rule 20.11 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_11.c>`_
      -  不适用

         .. _MisraC_Rule_20_12:
    * -  118
      -  用作 # 或 ## 运算符操作数的宏参数，如果它本身还会被进一步宏替换，则只能用作这些运算符的操作数
      -  `Rule 20.12 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_12.c>`_
      -  不适用

         .. _MisraC_Rule_20_13:
    * -  119
      -  第一个记号是 # 的行应是有效的预处理指令
      -  `Rule 20.13 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_13.c>`_
      -  不适用

         .. _MisraC_Rule_20_14:
    * -  120
      -  所有 #else、#elif 和 #endif 预处理指令都应与它们所关联的 #if、#ifdef 或 #ifndef 指令位于同一文件中
      -  `Rule 20.14 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_14.c>`_
      -  不适用

         .. _MisraC_Rule_21_1:
    * -  121
      -  不得对保留标识符或保留宏名使用 #define 和 #undef
      -  `Rule 21.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_01.c>`_
      -  `DCL37-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL37-C.+Do+not+declare+or+define+a+reserved+identifier>`_

         .. _MisraC_Rule_21_2:
    * -  122
      -  不得声明保留标识符或保留宏名
      -  `Rule 21.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_02.c>`_
      -  `DCL37-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL37-C.+Do+not+declare+or+define+a+reserved+identifier>`_

         .. _MisraC_Rule_21_3:
    * -  123
      -  不得使用 <stdlib.h> 的内存分配和释放函数
      -  `Rule 21.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_03.c>`_
      -  | `API03-C <https://wiki.sei.cmu.edu/confluence/display/c/API03-C.+Create+consistent+interfaces+and+capabilities+across+related+functions>`_
         | `API04-C <https://wiki.sei.cmu.edu/confluence/display/c/API04-C.+Provide+a+consistent+and+usable+error-checking+mechanism>`_
         | `MSC24-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC24-C.+Do+not+use+deprecated+or+obsolescent+functions>`_

         .. _MisraC_Rule_21_4:
    * -  124
      -  不得使用标准头文件 <setjmp.h>
      -  `Rule 21.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_04.c>`_
      -  不适用

         .. _MisraC_Rule_21_6:
    * -  125
      -  不得使用标准库的输入/输出函数
      -  `Rule 21.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_06.c>`_
      -  不适用

         .. _MisraC_Rule_21_7:
    * -  126
      -  不得使用 <stdlib.h> 的 atof、atoi、atol 和 atoll 函数
      -  `Rule 21.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_07.c>`_
      -  不适用

         .. _MisraC_Rule_21_9:
    * -  127
      -  不得使用 <stdlib.h> 的库函数 bsearch 和 qsort
      -  `Rule 21.9 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_09.c>`_
      -  不适用

         .. _MisraC_Rule_21_11:
    * -  128
      -  不得使用标准头文件 <tgmath.h>
      -  `Rule 21.11 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_11.c>`_
      -  不适用

         .. _MisraC_Rule_21_12:
    * -  129
      -  不应使用 <fenv.h> 的异常处理功能
      -  `Rule 21.12 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_12.c>`_
      -  不适用

         .. _MisraC_Rule_21_13:
    * -  130
      -  传递给 <ctype.h> 中函数的任何值都应能表示为 unsigned char，或者为值 EOF
      -  `Rule 21.13 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_13.c>`_
      -  不适用

         .. _MisraC_Rule_21_14:
    * -  131
      -  不得使用标准库函数 memcmp 比较以空字符结尾的字符串
      -  `Rule 21.14 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_14.c>`_
      -  不适用

         .. _MisraC_Rule_21_15:
    * -  132
      -  标准库函数 memcpy、memmove 和 memcmp 的指针参数应是指向兼容类型的限定或非限定版本的指针
      -  `Rule 21.15 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_15.c>`_
      -  不适用

         .. _MisraC_Rule_21_16:
    * -  133
      -  标准库函数 memcmp 的指针参数应指向指针类型、本质有符号类型、本质无符号类型、本质布尔类型或本质枚举类型中的一种
      -  `Rule 21.16 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_16.c>`_
      -  不适用

         .. _MisraC_Rule_21_17:
    * -  134
      -  使用 <string.h> 中的字符串处理函数时，不得访问超出其指针参数所引用对象边界的位置
      -  `Rule 21.17 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_17.c>`_
      -  不适用

         .. _MisraC_Rule_21_18:
    * -  135
      -  传递给 <string.h> 中任何函数的 size_t 参数应具有适当的值
      -  `Rule 21.18 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_18.c>`_
      -  不适用

         .. _MisraC_Rule_21_19:
    * -  136
      -  标准库函数 localeconv、getenv、setlocale 或 strerror 返回的指针只能以指向 const 限定类型的指针的方式来使用
      -  `Rule 21.19 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_19.c>`_
      -  不适用

         .. _MisraC_Rule_21_20:
    * -  137
      -  标准库函数 asctime、ctime、gmtime、localtime、localeconv、getenv、setlocale 或 strerror 返回的指针，在同名函数的后续调用之后不得再使用
      -  `Rule 21.20 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_20.c>`_
      -  不适用

         .. _MisraC_Rule_22_1:
    * -  138
      -  通过标准库函数动态获得的所有资源都应显式释放
      -  `Rule 22.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_01.c>`_
      -  不适用

         .. _MisraC_Rule_22_2:
    * -  139
      -  只有通过标准库函数分配的内存块才可以被释放
      -  `Rule 22.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_02.c>`_
      -  不适用

         .. _MisraC_Rule_22_3:
    * -  140
      -  同一文件不得同时在不同的流上以读写方式打开
      -  `Rule 22.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_03.c>`_
      -  不适用

         .. _MisraC_Rule_22_4:
    * -  141
      -  不得尝试向以只读方式打开的流写入
      -  `Rule 22.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_04.c>`_
      -  不适用

         .. _MisraC_Rule_22_5:
    * -  142
      -  不得解引用指向 FILE 对象的指针
      -  `Rule 22.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_05.c>`_
      -  不适用

         .. _MisraC_Rule_22_6:
    * -  143
      -  在关联的流关闭之后，不得使用指向 FILE 的指针的值
      -  `Rule 22.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_06.c>`_
      -  不适用

         .. _MisraC_Rule_22_7:
    * -  144
      -  宏 EOF 只应与能够返回 EOF 的任何标准库函数未经修改的返回值进行比较
      -  `Rule 22.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_07.c>`_
      -  不适用

         .. _MisraC_Rule_22_8:
    * -  145
      -  在调用会设置 errno 的函数之前，应将 errno 的值设为零
      -  `Rule 22.8 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_08.c>`_
      -  不适用

         .. _MisraC_Rule_22_9:
    * -  146
      -  在调用会设置 errno 的函数之后，应将 errno 的值与零进行比较
      -  `Rule 22.9 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_09.c>`_
      -  不适用

         .. _MisraC_Rule_22_10:
    * -  147
      -  只有当最后调用的函数是会设置 errno 的函数时，才可以检查 errno 的值
      -  `Rule 22.10 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_10.c>`_
      -  不适用

附加规则
********

规则 A.1：条件编译
==================
严重性
  必需

描述
  不要在头文件中条件编译函数声明。不要在头文件中条件编译结构体声明。可以条件排除结构体定义中的字段，以便在它们所支持的特性未启用时避免浪费内存。

理由
  基于编译期选项把头文件中的声明排除在外，可能会导致无法生成这些声明的文档。当代码路径需要根据所选选项变化时，这些声明的缺失也会使 ``if (IS_ENABLED(CONFIG_FOO)) {}`` 无法作为预处理条件表达式的替代方案使用。

.. _coding_guideline_inclusive_language:

规则 A.2：包容性语言
====================
严重性
  必需

描述
  不要引入下面列出的冒犯性术语的新用法。本规则适用于源代码、注释、文档和分支名称，但不限于这些。替代术语可能因领域或子系统而异，但应尽可能遵循更新后的行业标准。

  在维护现有实现，或为 Zephyr 项目外部管理的行业标准规范添加新实现时，允许有例外。

  建议在更新后的行业标准规范发布或管理机构公开宣布新术语后，尽快更改现有用法；如果没有任何规范适用，则应立即更改。

  .. list-table::
     :header-rows: 1

     * - 冒犯性术语
       - 建议的替代术语

     * - ``{master,leader} / slave``
       - - ``{primary,main} / {secondary,replica}``
         - ``{initiator,requester} / {target,responder}``
         - ``{controller,host} / {device,worker,proxy,target}``
         - ``director / performer``
         - ``central / peripheral``

     * - ``blacklist / whitelist``
       - * ``denylist / allowlist``
         * ``blocklist / allowlist``
         * ``rejectlist / acceptlist``

     * - ``grandfather policy``
       - * ``legacy``

     * - ``sanity``
       - * ``coherence``
         * ``confidence``

理由
  冒犯性术语无法营造包容的社区环境，因此违反了 Zephyr 项目的 `Code of Conduct`_。本编码规则受到 `Linux`_ 中类似规则的启发。

  .. _Code of Conduct: https://github.com/zephyrproject-rtos/zephyr/blob/main/CODE_OF_CONDUCT.md
  .. _Linux: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=49decddd39e5f6132ccd7d9fdc3d7c470b0061bb

状态
  相关的 GitHub Issue 和 Pull Request 会打上 `Inclusive Language Label`_ 标签。

  .. list-table::
     :header-rows: 1

     * - 领域
       - 选定的替代术语
       - 状态

     * - :ref:`蓝牙 <bluetooth_api>`
       - 请参阅 `Bluetooth Appropriate Language Mapping Tables`_
       -

     * - CAN
       - 这篇 `CAN in Automation Inclusive Language news post`_ 列出了一般性建议。关于规范文档更新中应使用的术语，请参阅 `CAN in Automation Inclusive Language`_。
       -

     * - eSPI
       - * ``master / slave`` => ``controller / target``
       - 关于新术语，请参阅 `eSPI Specification`_

     * - gPTP
       - * ``master / slave`` => TBD
       -

     * - :ref:`i2c_api`
       - * ``master / slave`` => ``controller / target``
       - 关于新术语，请参阅 `I2C Specification`_。

     * - :ref:`i2s_api`
       - * ``master / slave`` => ``controller / target``
       - 关于新术语，请参阅 `I2S Specification`_。Zephyr I2S API 已在 Zephyr 4.4 中迁移到这些术语；原有的宏名称作为已弃用的别名保留，并将在 Zephyr 5.0 中移除。

     * - SMP/AMP
       - * ``master / slave`` => TBD
       -

     * - :ref:`spi_api`
       - * ``master / slave`` => ``controller / peripheral``
         * ``MOSI / MISO / SS`` => ``SDO / SDI / CS``
       - Open Source Hardware Association 选定了这些替代术语。请参阅 `OSHWA Resolution to Redefine SPI Signal Names`_。Zephyr SPI API 和代码树已在 v4.5 中迁移到这些术语；原有名称作为兼容性别名保留，自 v4.5 起弃用，并计划在 v5.0 中移除。

     * - :ref:`twister_script`
       - * ``platform_whitelist`` => ``platform_allow``
         * ``sanitycheck`` => ``twister``
       -

  .. _Inclusive Language Label: https://github.com/zephyrproject-rtos/zephyr/issues?q=label%3A%22Inclusive+Language%22
  .. _I2C Specification: https://www.nxp.com/docs/en/user-guide/UM10204.pdf
  .. _I2S Specification: https://www.nxp.com/docs/en/user-manual/UM11732.pdf
  .. _Bluetooth Appropriate Language Mapping Tables: https://specificationrefs.bluetooth.com/language-mapping/Appropriate_Language_Mapping_Table.pdf
  .. _OSHWA Resolution to Redefine SPI Signal Names: https://oshwa.org/resources/a-resolution-to-redefine-spi-signal-names/
  .. _CAN in Automation Inclusive Language news post: https://www.can-cia.org/news/archive/view/?tx_news_pi1%5Bnews%5D=699&tx_news_pi1%5Bday%5D=6&tx_news_pi1%5Bmonth%5D=12&tx_news_pi1%5Byear%5D=2020&cHash=784e79eb438141179386cf7c29ed9438
  .. _CAN in Automation Inclusive Language: https://can-newsletter.org/canopen/categories/
  .. _eSPI Specification: https://downloadmirror.intel.com/27055/327432%20espi_base_specification%20R1-5.pdf


.. _coding_guideline_libc_usage_restrictions_in_zephyr_kernel:

规则 A.3：宏名称冲突
====================
严重性
  必需

描述
  ``MIN``、``MAX``、``ARRAY_SIZE`` 这类常用名称的宏，不得为了避开与其他实现的名称冲突而修改或加保护。特别地，不得为它们添加前缀以放入 Zephyr 专用的命名空间，不得使用 ``#undef`` 重新定义，也不得使用 ``#ifndef`` 条件排除其编译。反之，如果与来自 :ref:`模块 <modules>` 的既有定义发生冲突，则需要修改该模块自身的代码，最好在上游修改，或者通过 Zephyr 自己分支中的改动来实现。

  本规则普遍适用于 Zephyr 项目，与宏的引入时间或它在代码树中的当前名称无关。如果某个宏名称在其他几个知名开源项目中普遍使用，那么 Zephyr 中的实现就应使用该名称。虽然“普遍使用”的含义带有主观且无法量化的成分，但最终目标是向用户提供他们熟悉的宏。

  最后，本规则同样适用于模块之间的名称冲突：在这种情况下，应在引入这两个模块之前，将它们修改为使用发生冲突的宏名称的模块专属版本。

理由
  Zephyr 是一个 RTOS，它以模块的形式带来额外的功能和依赖。这些模块通常是独立的项目，可能会使用与其他模块或 Zephyr 本身冲突的宏名称。由于在本文档的语境中 Zephyr 被视为核心或主项目，因此它应实现不带命名空间的宏版本。鉴于 Zephyr 为每个模块都使用了相应上游的分支，总是可以通过修补各模块中的宏实现来避免冲突。

规则 A.4：Zephyr 内核中 C 标准库的使用限制
==========================================
严重性
  必需

描述
  Zephyr 内核中 C 标准库函数和宏的使用应限于 ISO/IEC 9899:2011 标准（也称为 C11）中的以下函数和宏及其扩展：

  .. csv-table:: Zephyr 内核中允许使用的 libc 函数和宏列表
     :header: 函数,来源
     :widths: auto

     abort(),ISO/IEC 9899:2011
     abs(),ISO/IEC 9899:2011
     aligned_alloc(),ISO/IEC 9899:2011
     assert(),ISO/IEC 9899:2011
     atoi(),ISO/IEC 9899:2011
     bsearch(),ISO/IEC 9899:2011
     calloc(),ISO/IEC 9899:2011
     exit(),ISO/IEC 9899:2011
     fprintf(),ISO/IEC 9899:2011
     fputc(),ISO/IEC 9899:2011
     fputs(),ISO/IEC 9899:2011
     free(),ISO/IEC 9899:2011
     fwrite(),ISO/IEC 9899:2011
     gmtime(),ISO/IEC 9899:2011
     isalnum(),ISO/IEC 9899:2011
     isalpha(),ISO/IEC 9899:2011
     iscntrl(),ISO/IEC 9899:2011
     isdigit(),ISO/IEC 9899:2011
     isgraph(),ISO/IEC 9899:2011
     isprint(),ISO/IEC 9899:2011
     isspace(),ISO/IEC 9899:2011
     isupper(),ISO/IEC 9899:2011
     isxdigit(),ISO/IEC 9899:2011
     labs(),ISO/IEC 9899:2011
     llabs(),ISO/IEC 9899:2011
     malloc(),ISO/IEC 9899:2011
     memchr(),ISO/IEC 9899:2011
     memcmp(),ISO/IEC 9899:2011
     memcpy(),ISO/IEC 9899:2011
     memmove(),ISO/IEC 9899:2011
     memset(),ISO/IEC 9899:2011
     perror(),ISO/IEC 9899:2011
     printf(),ISO/IEC 9899:2011
     putc(),ISO/IEC 9899:2011
     putchar(),ISO/IEC 9899:2011
     puts(),ISO/IEC 9899:2011
     qsort(),ISO/IEC 9899:2011
     rand(),ISO/IEC 9899:2011
     realloc(),ISO/IEC 9899:2011
     snprintf(),ISO/IEC 9899:2011
     sprintf(),ISO/IEC 9899:2011
     sqrt(),ISO/IEC 9899:2011
     sqrtf(),ISO/IEC 9899:2011
     srand(),ISO/IEC 9899:2011
     strcat(),ISO/IEC 9899:2011
     strchr(),ISO/IEC 9899:2011
     strcmp(),ISO/IEC 9899:2011
     strcpy(),ISO/IEC 9899:2011
     strcspn(),ISO/IEC 9899:2011
     strerror(),ISO/IEC 9899:2011
     strlen(),ISO/IEC 9899:2011
     strncat(),ISO/IEC 9899:2011
     strncmp(),ISO/IEC 9899:2011
     strncpy(),ISO/IEC 9899:2011
     `strnlen()`_,POSIX.1-2008
     strrchr(),ISO/IEC 9899:2011
     strspn(),ISO/IEC 9899:2011
     strstr(),ISO/IEC 9899:2011
     strtol(),ISO/IEC 9899:2011
     strtoll(),ISO/IEC 9899:2011
     strtoul(),ISO/IEC 9899:2011
     strtoull(),ISO/IEC 9899:2011
     time(),ISO/IEC 9899:2011
     tolower(),ISO/IEC 9899:2011
     toupper(),ISO/IEC 9899:2011
     vfprintf(),ISO/IEC 9899:2011
     vprintf(),ISO/IEC 9899:2011
     vsnprintf(),ISO/IEC 9899:2011
     vsprintf(),ISO/IEC 9899:2011

  上面列出的所有函数都必须由 :ref:`minimal libc <c_library_minimal>` 实现，以确保 Zephyr 内核能够使用 minimal libc 构建。

  此外，上述列表中不属于 ISO/IEC 9899:2011 标准的任何函数都必须由 :ref:`common libc <c_library_common>` 实现，以确保它们在多种 C 标准库中都可用。

  在满足上述要求的前提下，如果有正当理由，允许向 Zephyr 内核引入新的 C 标准库函数。

  请注意，上面列出的函数的使用仍受安全可靠编码实践的约束，不应因为本规则列出了它们，就认为在 Zephyr 内核中使用它们是无条件允许的。

  在此语境中，“Zephyr 内核”由以下组件组成：

  * 内核（ :file:`kernel` ）
  * OS 库（ :file:`lib/os` ）
  * 架构移植层（ :file:`arch` ）
  * 日志子系统（ :file:`subsys/logging` ）

理由
  Zephyr 内核必须能够使用 :ref:`minimal libc <c_library_minimal>` 构建，这是 Zephyr RTOS 的一部分、由 Zephyr 项目维护的一个精简 C 标准库实现，从而可以对内核和核心 OS 服务进行自包含的测试和验证。

  为了确保 Zephyr 内核能够使用 minimal libc 构建，有必要将 Zephyr 内核中 C 标准库函数和宏的使用限制为 minimal libc 所提供的那些函数和宏。

规则 A.5：Zephyr 代码库中 C 标准库的使用限制
============================================
严重性
  必需

描述
  Zephyr 代码库中 C 标准库函数和宏的使用应限于 ISO/IEC 9899:2011 标准（也称为 C11）中的函数，但不包括附录 K“边界检查接口”，除非本规则另有豁免。

  在此语境中，“Zephyr 代码库”指提交到 `main Zephyr repository`_ 的所有嵌入式源代码文件，但不包括 :ref:`coding_guideline_libc_usage_restrictions_in_zephyr_kernel` 所定义的 Zephyr 内核。嵌入式源代码指要在嵌入式目标上执行的代码，因此不包括主机工具，也不包括专用于 :ref:`native <boards_posix>` 测试目标的代码。

  以下非 ISO 9899:2011 的函数和宏（下称非标准函数和宏）不受本规则约束，允许在 Zephyr 代码库中使用：

  .. csv-table:: 允许使用的非标准 libc 函数列表
     :header: Function,Source
     :widths: auto

     `gmtime_r()`_,POSIX.1-2001
     `strnlen()`_,POSIX.1-2008
     `strtok_r()`_,POSIX.1-2001

  上面列出的所有非标准函数和宏都必须由 :ref:`common libc <c_library_common>` 实现，以确保在使用未实现这些函数的 C 标准库时也能提供这些函数。

  在满足上述要求的前提下，如果有正当理由，允许将常见 C 标准库中的新非标准函数加入上述列表。但是，如果存在功能等价的标准函数，则应使用该标准函数。

理由
  一些 C 标准库（例如 Newlib 和 Picolibc）包含由扩展 ISO C 标准的各种标准和事实标准（例如 POSIX、Linux）所定义的额外函数和宏。

  ISO/IEC 9899:2011 标准并不要求 C 编译器工具链支持这些非标准函数，因此使用这些函数可能会导致与自带 C 标准库的第三方工具链出现兼容性问题。

  .. _main Zephyr repository: https://github.com/zephyrproject-rtos/zephyr
  .. _gmtime_r(): https://pubs.opengroup.org/onlinepubs/9699919799/functions/gmtime_r.html
  .. _strnlen(): https://pubs.opengroup.org/onlinepubs/9699919799/functions/strlen.html
  .. _strtok_r(): https://pubs.opengroup.org/onlinepubs/9699919799/functions/strtok.html
