FROM ubuntu:22.04

# Add sources list and install dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-dev

# cp requirements.txt \
COPY requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple

