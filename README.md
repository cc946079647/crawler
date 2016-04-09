#基本说明
crawler是一个使用python实现的爬虫框架，提供下载网页、解析网页内容的功能。目前处于开发阶段。

#模块
##config.py
配置管理模块，管理整个爬虫框架的配置信息。  
config采用分层结构管理所有的配置，每一项配置适应name索引。每一层的config按照相同的方式组织。目前的cinfig的层次为：  
###config###
+ __downloader__
    + __agent string__:下载器标志，用于伪装爬虫
    + __save_page__:是否保存下载页面，默认为False
    + __save_parsed__:是否保存解析得到的内容，默认为True
+ __parser__
    + __method__:解析器采用的解析方法，可选css或tag。css使用css语法的选择器；tag根据tag的属性和text内容过滤。  
    + __tag__:对每个希望得到的标签定义相应的tag，例如，希望抽取超链接中的地址，那么需要设置config[a]。config[tag]也采用key-value形式组织对这一个标签的设置。  
        1. __method=css时__，tag对应的是一个列表，列表至少包括2项：
            + __css expression__:string,css格式的选择器。对每一个tag只能有一个css expression。
            + __seek__:string，希望得到的与tag相关的信息。希望获得属性时设置为属性名，希望获得文本时设置为text，希望得到整个tag时设置为all，设置项数至少为1项。
                                注意，如果使用css expression得到的tag有内嵌的tag，那么text会包含内嵌tag的文本。  
        2. __method=tag时__，tag对应的是一个字典，字典可以包括3项：
            + __attr__:可选，string,希望得到的tag的属性要求，正则表达式。
            + __text__:可选，string，希望得到的tag的文本要求，正则表达式。例如，希望得到tag的text为数字：[0-9]+。
            + __seek__:必须，与__method=css__时的__seek__相同。列表，列表的每一项代表希望得到的属性、文本或整个tag。至少包含1项。
+ __IO__
    + __file_name_tran_table__:列表，可选。默认使用URL保存爬取页面和解析内容，URL中的"/、\、?、："不能作为文件名，需要替换。file_name_tran_table的第一项是需要替换的字符组成的字符串，第二项是每一个被替换的字符被换为的字符组成的字符串。  
                                   例如，将"/、\、?、："全部替换为"_"时可设置：["/\\?：","____"]。  
                                   
####待完善功能
- 整理默认配置信息，写入文件
- 从文件解析配置信息，不要硬编码在代码中


##downloader.py
下载器，目前以单线程实现。downloader从urllist获取url，下载页面，并使用parser解析页面。

####待完善功能
- 多线程实现
- 完善多线程下操作：url队列为空时阻塞/定时等待；完成下载后通知url队列

##parser.py
基于beautifulsoup的html解析模块，针对过滤条件的不同情况，提供两种过滤方式：
#### 条件精确时：要求提供需要标签的属性值和text信息，以正则表达式方式给出。
#### 采用css选择器，要求提供提取需要信息的css选择器，以string方式给出。  
parser的返回结果基于tag组织，使用dict将tag映射到每个tag的解析结果。每个tag的解析结果也采用dict组织。具体形式如下
###res###
+ __tag1__
    + __seek1__:list，每一项是一个tag中得到的seek1过滤结果。
    + __seek2__:list，每一项是一个tag中得到的seek2过滤结果。
    + __\.\.\.__:
+ __tag2__
    + __seek1__:
    + __seek2__:
    + __seek3__:
    + __\.\.\.__:
+ __\.\.\.__  
###例如，希望获取页面中超链接的地址，结果组织形式如下###
+ __a__
    + __href__:超链接组成的list

##urllist.py
url队列模块，管理待爬取url和一下在url信息。支持多线程同时访问。
####待完善功能
- 提供下载器完成url下载后的回调方法
- 中文编码问题


##logger.py
日志模块，记录信息
####待完善功能
- 采用第三方日志库