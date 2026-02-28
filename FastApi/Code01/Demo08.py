## 请求体
## 接下来我们创建了一个 /items/ 路由，使用 @app.post 装饰器表示这是一个处理 POST 请求的路由。
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/")
def create_item(item: Item):
    return item

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)