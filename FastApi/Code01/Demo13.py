import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    content = {"item_id": item_id}
    headers = {"X-Custom-Header": "custom-header-value"}
    return JSONResponse(content=content, headers=headers)

# 自定义响应头
# 使用 JSONResponse 自定义响应头:

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)