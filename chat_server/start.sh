#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

docker run \
  -it \
  --rm \
  --network=host \
  --name chat_server_9010 \
  --gpus "device=0" \
  --shm-size 32G \
  -v "$SCRIPT_DIR:/chat_server" \
  -w /chat_server \
  chat_server:v1.0 \
  python3 main.py --port 9010 --model_path model/qwen2-7b-instrust-awq-q4_K_M.gguf