 docker run \
    -it \
    --rm \
    --name embedding_server \
    --network=host \
    --gpus all \
    --shm-size 32G \
    -v /home/mozinode4p/.cache/huggingface/hub/:/root/.cache/huggingface/hub/ \
    -v /home/mozinode4p/PycharmProjects/embedding_server/:/embedding_server/ \
    -w /embedding_server \
    chat_server:v1.0 \
    python3 main.py