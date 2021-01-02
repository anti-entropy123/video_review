# 名称: 视频审阅平台后端

# 功能: docker部署测试

# 日期: 2020 12 22

FROM ubuntu:latest
USER root

# MAINTAINER yjn "1348651580@qq.com"
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list; apt-get clean; apt-get -y update; apt-get -y upgrade
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
# RUN apt-get -y install mongodb
RUN DEBIAN_FRONTEND=noninteractive apt install -y libgl1-mesa-glx
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libglib2.0-0
RUN apt-get install -y libsm6 libxext6
RUN apt-get install -y libxrender-dev
RUN pip3 install virtualenv -i https://pypi.douban.com/simple

# VOLUME /var/lib/mongodb/
# VOLUME /home/video_review/back-end
COPY ./server src
WORKDIR /src
RUN virtualenv venv --python=python3.8
RUN /bin/bash -c "source venv/bin/activate"
RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple
# RUN pip3 install -U cos-python-sdk-v5 -i https://pypi.douban.com/simple
EXPOSE 443 
EXPOSE 1314 
RUN mkdir /tmp/video_review/

CMD ["python3", "main.py", "1>server.log", "2>server.log"]