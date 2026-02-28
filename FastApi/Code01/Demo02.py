from typing import Optional

import uvicorn
from fastapi import FastAPI

app = FastAPI()


## 两个路由进行操作
@app.get("/")
def read_root():
    return {"hello": "world"}

@app.get("/items/{item_id}")
## q: Optional[str]表示?q=keyword，也就是一个param
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
