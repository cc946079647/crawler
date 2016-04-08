#基本说明
crawler是一个使用python实现的爬虫框架，提供下载网页、解析网页内容的功能。目前处于开发阶段。

#模块
##config.py
配置管理模块，管理整个爬虫框架的配置信息。
最高层的configuration为每个模块提供各自的配置信息，每个模块的配置信息也采用dict管理。

###downloader config
####下载器设置，包含下面的属性
- agent 爬虫的agent设置，用于模仿浏览器
- save_page 	是否保存爬取的页面
- save_parsed   是否保存解析得到的内容


###parser config
####解析器配置，包含下面的属性
- method:css/tag 使用哪一种方法解析html
- method == css:配置信息是一个list，第一项是css表达式；后面的是希望提取的属性名，all表示提取整个标签。
- example：['h3 > a',href]，提取h3标签中的a标签的href属性
- method = tag:配置信息是一个dict，对每一个标签有下面的dict进行设置：
- attr:设置提取的标签在属性上的要求，正则表达式形式
- text:设置提取的标签在文本上的要求，正则表达式形式
- example:{attr:'href',text:'[0-9]+'}，提取包含href属性，且文本内容是数字的标签

###IO config
####IO操作设置，包含下面的属性
- file_name_trans_table:由于使用url作为文件名，url中的一些字符(/、\、？、：)不能作为文件名，需要替换为其他字符。
  是一个list，第一项是需要被替换的字符组成的字符串，第二项是被替换成的字符组成的字符串，二者一一对应。
- example:file_name_tran_table=['/\\?:','____'],将'/\\?:'全部替换为'_'
####待完善功能
- 整理默认配置信息，写入文件
- 从文件解析配置信息

##downloader.py
下载器，目前以单线程实现。downloader从urllist获取url，下载页面，并使用parser解析页面。
####待完善功能
- 多线程实现
- 完善多线程下操作：url队列为空时阻塞/定时等待；完成下载后通知url队列

##parser.py
基于beautifulsoup的html解析模块，针对过滤条件的不同情况，提供两种过滤方式：
#### 条件精确时：要求提供需要标签的属性值和text信息，以正则表达式方式给出。
#### 采用css选择器，要求提供提取需要信息的css选择器，以string方式给出。

##urllist.py
url队列模块，管理待爬取url和一下在url信息。支持多线程同时访问。
####待完善功能
- 提供下载器完成url下载后的回调方法
- 中文编码问题

##logger.py
日志模块，记录信息
####待完善功能
- 采用起三方日志库