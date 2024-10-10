#!/bin/bash
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

docker run \
  -it \
  --rm \
  --name vllm_test \
  --network=host \
  --shm-size 32G \
  --gpus "device=0" \
  -v "$SCRIPT_DIR:/palapa/" \
  -w /palapa/ \
  vllm:v1.0