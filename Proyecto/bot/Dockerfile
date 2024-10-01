FROM debian:stretch-slim AS chatscript-base
ENV DEBIAN_FRONTEND noninteractive
SHELL ["/bin/bash", "-c"]

RUN echo "deb http://archive.debian.org/debian stretch stretch-security main contrib non-free" > /etc/apt/sources.list

RUN apt-get update -y
RUN apt-get install -y autoconf unzip curl

RUN mkdir -p /ChatScript/
WORKDIR /opt/alloxentric/ChatScript/
RUN curl -LO https://github.com/ChatScript/ChatScript/archive/11.5.zip
RUN unzip 11.5.zip && mv ChatScript-11.5/* . && rm -rf ChatScript-11.5 11.5.zip

WORKDIR /opt/alloxentric/
RUN chmod +x /opt/alloxentric/ChatScript/BINARIES/LinuxChatScript64

