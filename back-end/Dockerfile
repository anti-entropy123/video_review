# 名称: 视频审阅平台后端

# 功能: docker部署测试

# 日期: 2020 11 05

FROM ubuntu:latest
USER root

# MAINTAINER yjn "1348651580@qq.com"

# COPY venv /src/venv

COPY server /src

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get clean
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN pip3 install virtualenv -i https://pypi.douban.com/simple
RUN apt-get -y install mongodb

WORKDIR /src
RUN virtualenv venv --python=python3.8
# RUN cd venv/bin/
RUN /bin/bash -c "source venv/bin/activate"
# RUN cd ../../
# RUN ls
RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple
RUN pip3 install -U cos-python-sdk-v5 -i https://pypi.douban.com/simple
EXPOSE 1314
RUN service mongodb start
CMD python3 main.py