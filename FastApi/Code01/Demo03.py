from typing import Optional

import uvicorn
from fastapi import FastAPI

# 这个进行FastAPI 交互式 API 文档
"""
FastAPI 提供了内置的交互式 API 文档，使开发者能够轻松了解和测试 API 的各个端点。

这个文档是自动生成的，基于 OpenAPI 规范，支持 Swagger UI 和 ReDoc 两种交互式界面。

通过 FastAPI 的交互式 API 文档，开发者能够更轻松地理解和使用 API，提高开发效率

在运行 FastAPI 应用时，Uvicorn 同时启动了交互式 API 文档服务。

默认情况下，你可以通过访问 http://127.0.0.1:8000/docs 来打开 Swagger UI 风格的文档：

Swagger UI 提供了一个直观的用户界面，用于浏览 API 的各个端点、查看请求和响应的结构，并支持直接在文档中进行 API 请求测试。通过 Swagger UI，你可以轻松理解每个路由操作的输入参数、输出格式和请求示例。

或者通过 http://127.0.0.1:8000/redoc 来打开 ReDoc 风格的文档。
"""

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
## q: Optional[str]表示?q=keyword，也就是一个param
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc

## FastAPI 自带的文档界面（Swagger UI 和 ReDoc）为了保持轻量，默认是从国外的 CDN（jsdelivr）加载样式和脚本文件的。
# 由于网络环境原因（你懂的），国内访问这个 CDN 经常不稳定或者直接被阻断，导致文件下载失败，页面自然就是一片空白。