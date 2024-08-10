FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04

# Add sources list and install dependencies
ADD source.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-dev \
    vim \
    git \
    cmake \
    wget

# Install Llama Factory requirements
RUN pip3 install torch \
    --no-cache-dir -i https://download.pytorch.org/whl/cu121/

RUN pip3 install transformers \
    datasets \
    accelerate \
    peft \
    trl \
    gradio \
    deepspeed \
    modelscope \
    ipython \
    scipy \
    einops \
    sentencepiece \
    protobuf \
    jieba \
    rouge-chinese \
    nltk \
    sse-starlette \
    matplotlib \
    pandas \
    numpy \
    tqdm \
    tensor_parallel \
    scikit-learn \
    ninja \
    packaging \
    gguf \
    tiktoken \
    --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple

# Install FlagEmbedding
RUN pip install -U FlagEmbedding --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple

