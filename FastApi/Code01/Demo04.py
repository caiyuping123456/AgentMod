from typing import Optional

import uvicorn
from anthropic import BaseModel
from fastapi import FastAPI

# 接下来我们修改 main.py 文件来从 PUT 请求中接收请求体。
# 我们借助 Pydantic 来使用标准的 Python 类型声明请求体。

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[str] = None

@app.get("/")
def read_root():
    return {"hello": "world"}
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)