# 将官方 Python 运行时用作父镜像
FROM python:3.7
# 将当前目录内容复制到位于 /myapps 中的容器中
ADD . .
COPY requirements.txt ./
COPY gunicorn.conf ./
# 安装 requirements.txt 中指定的任何所需软件包
RUN pip install -r requirements.txt -i  https://mirrors.aliyun.com/pypi/simple/
# 定义环境变量
#ENV NAME World
# 在容器启动时运行 app.py
CMD ["gunicorn", "app:app", "-c", "gunicorn.conf"]
