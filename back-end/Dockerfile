# 名称: 视频审阅平台后端

# 功能: docker部署测试

# 日期: 2020 12 22

FROM ubuntu:latest
USER root

# MAINTAINER yjn "1348651580@qq.com"

COPY server /src

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list; apt-get clean; apt-get -y update; apt-get -y upgrade
RUN apt-get -y install python3 python3-pip mongodb
RUN DEBIAN_FRONTEND=noninteractive apt install -y libgl1-mesa-glx
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libglib2.0-0
RUN apt-get install -y libsm6 libxext6
RUN apt-get install -y libxrender-dev
RUN pip3 install virtualenv -i https://pypi.douban.com/simple
WORKDIR /src
RUN virtualenv venv --python=python3.8
# RUN cd venv/bin/
RUN /bin/bash -c "source venv/bin/activate"
# RUN cd ../../
# RUN ls
RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple
# RUN pip3 install -U cos-python-sdk-v5 -i https://pypi.douban.com/simple
EXPOSE 1314
RUN service mongodb start

CMD python3 main.py