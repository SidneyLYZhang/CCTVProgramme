# README

定时读取直播节目单。

如果要匹配直播栏目，首先需要直播节目时间表。

每日一个文件，使用json格式保存（减少错误识别和处理）。

含相关解析方案。

- `gettingNow.py`：进行数据爬取。
- `Example_of_Parsing.ipynb`：简单的数据解析示例。
- `dataparse`：数据解析的方法。
- `data`：爬取到的数据。