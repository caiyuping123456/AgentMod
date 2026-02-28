import uvicorn
from fastapi import FastAPI

# 初始化FastAPI实例化对象
app = FastAPI()

# get请求
@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
