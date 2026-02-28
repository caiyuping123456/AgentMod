import uvicorn
from fastapi import Header, Cookie
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/items/")
def read_item(user_agent: str = Header(None), session_token: str = Cookie(None)):
    return {"User-Agent": user_agent, "Session-Token": session_token}

@app.get("/redirect")
def redirect():
    return RedirectResponse(url="/items/")

## 重定向和状态码
## 使用 RedirectResponse 实现重定向，将客户端重定向到 /items/ 路由。
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)