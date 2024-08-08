# Palapa Base Docker Image

本仓库包含用于构建 `palapa/base:v1.0` 镜像的 Dockerfile。此镜像基于 Ubuntu 22.04，并包含 Python 3.10 及其所需的依赖项。

### 构建镜像

在包含 Dockerfile 和 `requirements.txt` 的目录中运行以下命令以构建 Docker 镜像：

```sh
docker build -t palapa/base:v1.0 .
```