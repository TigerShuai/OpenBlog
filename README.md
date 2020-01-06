# 开源博客
OpenBlog项目更像是一个基于flask_appbuilder开源运营框架的组织内部的文本库。

------------


###1.该项目有三部分组成：
1. 有权限的组织内部文本库
2. 根据App端抓取多个交友软件女性数据源组成的供给公司营销人员使用的引流板块
3. 封装成小程序数据接口及运营端板块功能

###2.当前开源部分为组织内部文本库（博客）功能
项目演示地址：https://www.dogsrun.cn

####博客项目依赖于：
1. flask_appbuilder：[API参考](https://flask-appbuilder.readthedocs.io/en/latest/config.html#using-config-py "API参考")
2. 一款开源的、可嵌入的 Markdown 在线编辑器（组件）：[Editor.md](https://pandao.github.io/editor.md/ "Editor.md")
3. 图视频相关本地或链接上传使用到的阿里云OSS：[阿里云文档](https://help.aliyun.com/document_detail/88426.html?spm=a2c4g.11186623.6.848.47a34fa9W9gl8a "阿里云文档")
4. 数据库使用postgresql
5. 项目部署使用docker+gevent：[gevent文档](https://docs.gunicorn.org/en/latest/settings.html#config "gevent文档")

###3.项目快速启动需要配置的位置
####1. 项目configs/settings.py文件修改为自己的postgresql数据库路径

```python
import os
DEBUG = True
PROXY_FIX_APP = os.getenv('PROXY_FIX_APP', False)
***~~注意：docker启动，请修改127.0.0.1为postgresql的网关IPAddress地址~~***
default_user_db_uri = "postgresql://当前数据库用户:@127.0.0.1/数据库名"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default_user_db_uri)
```

####2. 项目configs/settings.py文件修改为自己的阿里云OSS相关

```python
# 阿里云图片处理相关
OSS_KEY = 'You_KEY'
OSS_SECRET = 'You_SECRET'
OSS_URL = 'Bucket 域名'
OSS_NAME = 'You_bucket_Name' #bucket 名称

OSS_IMGSNAME = 'imgs/' #imgs
OSS_VIDEO = 'video/'# video
USER_IP = '' #链接修改为自有域名调用，非必要设置
STATIC_UPLOAD_PATH = '/app/static/upload/'#本地上传路径
IMGS_TYPE = '?x-oss-process=style/bolgs' #样式相关，非必要设置
```
####3. 初始化数据库

```shell
#会在当前指定数据库下生成所有需要的数据表
flask fab create-db
#会创建超级管理员用户
flask fab create-admin
```

####4. 运行项目
```shell
1. flask run
2. 或者本地直接run ws_blogs.py文件
```

###4.项目演示
![](https://dogsrun.cn/imgs/20200106113131.png?x-oss-process=style/bolgs)

![](https://dogsrun.cn/imgs/20200106113219.png?x-oss-process=style/bolgs)


------------

###5.根据App端抓取多个交友软件女性数据源组成的供给公司营销人员使用的引流板块功能提前展示
####1.数据展示及简单的客户跟踪功能（联系方式已隐藏）
![](https://dogsrun.cn/imgs/20200106113652.png?x-oss-process=style/bolgs)
####2.用户引流进度
![](https://dogsrun.cn/imgs/20200106114408.png?x-oss-process=style/bolgs)
####3.单个用户多运营沟通节点展示
![](https://dogsrun.cn/imgs/20200106114559.png?x-oss-process=style/bolgs)
