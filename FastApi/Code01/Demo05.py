import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

"""
@app.get("/items/{item_id}")：定义了一个路由路径，其中 {item_id} 是路径参数，对应于函数参数 item_id。
def read_item(item_id: int, q: str = None)：路由处理函数接受一个整数类型的路径参数 item_id 和一个可选的字符串类型查询参数 q。
在路由操作中，可以使用函数参数声明查询参数。例如，q: str = None 表示 q 是一个可选的字符串类型查询参数，默认值为 None。
"""
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)