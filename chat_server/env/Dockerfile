FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04

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
    --no-cache-dir -i https://download.pytorch.org/whl/cu124/

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

# Install FlashAttention
RUN pip install flash-attn \
    --no-build-isolation \
    --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple

# Clone, build and install llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp && \
    cd llama.cpp && \
    cmake -B build -DGGML_CUDA=ON -DCMAKE_BUILD_RPATH=/usr/lib/x86_64-linux-gnu:/usr/local/cuda-12.4/compat && \
    cmake --build build --config Release -j 8 && \
    cd ..

# Install llama-cpp-python
RUN CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_BUILD_RPATH=/usr/lib/x86_64-linux-gnu:/usr/local/cuda-12.4/compat" \
    pip install llama-cpp-python