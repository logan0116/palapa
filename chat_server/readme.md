# Chat_server

中文：本地的量化大模型chat服务，基于llama.cpp，llama-cpp-python
基于Dockers部署，支持多个模型同时部署。

en: A local quantization large model chat service based on llama.cpp, llama-cpp-python
Deployed based on Dockers, supporting the deployment of multiple models at the same time.

## Dockerfile

[Dockerfile](env%2FDockerfile)

```Bash
# path: env
docker build -t chat_server:v1.0 .
```

## 服务

```python
import requests

inputs = '你好'
history = [
    {"role": "system", "content": "你是一个数控机床领域故障诊断助手"}
]

url = "http://[ip]:[port]/chat"
res = requests.post(url,
                    json={"inputs": inputs, "history": history},
                    timeout=60)

print(res.json()['date'])

```