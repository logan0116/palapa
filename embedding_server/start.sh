#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

docker run \
  -it \
  --rm \
  --name embedding_server \
  --network=host \
  --gpus all \
  --shm-size 32G \
  -v /home/mozinodej/.cache/huggingface/hub/:/root/.cache/huggingface/hub/ \
  -v "$SCRIPT_DIR:/embedding_server/" \
  -w /embedding_server \
  embedding_server:v1.0 \
  python3 main.py --port 9001