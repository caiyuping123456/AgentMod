import uvicorn
from fastapi import FastAPI

app = FastAPI()

# 路由处理函数返回一个字典，该字典将被 FastAPI 自动转换为 JSON 格式，并作为响应发送给客户端：
@app.get("/items/")
def read_item(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)