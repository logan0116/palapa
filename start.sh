#!/bin/bash
# 只启动一个容器 palapa_base

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

docker run \
  -d \
  --rm \
  --name palapa_base \
  --network=host \
  --shm-size 32G \
  -v "$SCRIPT_DIR:/palapa/" \
  -w /palapa/ \
  palapa/base:v1.0 \
  streamlit run webui/palapa.py --server.address 0.0.0.0 --server.port 8501