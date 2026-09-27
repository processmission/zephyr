.. SPDX-FileCopyrightText: Copyright The Process Mission

..
   SPDX-FileCopyrightText: Copyright The Zephyr Project Contributors
   SPDX-License-Identifier: Apache-2.0

.. _twister_console_harness:

控制台
######

``console`` 测试适配器让 Twister 使用测试 YAML 文件中定义的正则表达式解析测试文本输出。

目前支持以下选项：

type: <one_line|multi_line>（必填）
    取决于待匹配的正则表达式字符串。

regex: <list of regular expressions>（必填）
    用于匹配测试输出的正则表达式字符串，以确认测试按预期运行。

ordered: <True|False>（默认 False）
    按顺序或不按顺序检查正则表达式字符串。

record: <recording options>（可选）
  regex: <list of regular expressions>（必填）
    带命名子组的正则表达式，用于匹配测试实例输出行中的数据字段，以提取自定义数据供进一步分析。记录会写入构建目录的 ``recording.csv`` 文件，以及 ``twister.json`` 中测试套件对象的 ``recording`` 属性。

    提供多个正则表达式时，每个表达式都会应用于每一行输出，因此可能从同一行生成多条不同记录，也可能从不同行生成不同或相似的记录。

    CSV 文件的列数等于所有记录中检测到的字段总数，缺失值用空字符串填充。

    例如，提取 ``metric``、``cycles``、``nanoseconds`` 三个数据字段：

    .. code-block:: yaml

      record:
        regex:
          - "(?P<metric>.*):(?P<cycles>.*) cycles, (?P<nanoseconds>.*) ns"

  merge: <True|False>（默认 False）
    允许每个测试实例仅保留一条记录，其中包含正则表达式提取的全部字段。同名字段会按出现顺序合并为列表。根据正则表达式规则和测试输出，各多值字段包含的值数量可能不同。

  as_json: <list of regex subgroup names>（可选）
    正则表达式提取到命名子组的数据字段，还会按 JSON 编码字符串解析，并作为嵌套的 ``recording`` 对象属性写入 ``twister.json``。对应的 ``recording.csv`` 列保留原始 JSON 字符串。

    使用此选项，测试日志可以传递测试镜像输出的分层数据结构，包括汇总结果、跟踪数据和统计信息等，供进一步分析。

    例如，以下配置：

    .. code-block:: yaml

      record:
        regex: "RECORD:(?P<type>.*):DATA:(?P<metrics>.*)"
        as_json: [metrics]

    匹配以下测试日志字符串时：

    .. code-block:: none

      RECORD:jitter_drift:DATA:{"rollovers":0, "mean_us":1000.0}

    将在 ``twister.json`` 中报告为：

    .. code-block:: json

      "recording":[
          {
                "type":"jitter_drift",
                "metrics":{
                    "rollovers":0,
                    "mean_us":1000.0
                }
          }
      ]
