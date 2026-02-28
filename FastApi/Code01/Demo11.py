import uvicorn
from fastapi import Header, Cookie
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
def read_item(user_agent: str = Header(None), session_token: str = Cookie(None)):
    return {"User-Agent": user_agent, "Session-Token": session_token}

## 请求头和 Cookie
## 使用 Header 和 Cookie 类型注解获取请求头和 Cookie 数据。

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)