import uvicorn
from fastapi import FastAPI

app = FastAPI()


# 以下实例中我们定义了一个 /items/ 路由，接受两个查询参数 skip 和 limit，它们的类型均为整数，默认值分别为 0 和 10。
@app.get("/items/")
def read_item(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)