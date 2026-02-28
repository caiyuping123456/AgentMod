import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

## 路由处理函数返回一个 Pydantic 模型实例，FastAPI 将自动将其转换为 JSON 格式，并作为响应发送给客户端：

@app.post("/items/")
def create_item(item: Item):
    return item

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)