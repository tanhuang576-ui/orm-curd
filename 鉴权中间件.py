from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()
white_path = ["/", "/login","/docs","/redoc","/openapi.json"]
valid_token = "abc123xyz"

# 适配docs授权按钮
api_key = APIKeyHeader(name="token", auto_error=False)

class AuthMid(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in white_path:
            return await call_next(request)
        token = request.headers.get("token")
        if token != valid_token:
            raise HTTPException(status_code=401, detail="鉴权失败")
        return await call_next(request)

app.add_middleware(AuthMid)

@app.get("/login")
def login():
    return {"token": valid_token}

@app.get("/info")
def info():
    return {"msg":"用户数据"}
# uvicorn 鉴权中间件:app --reload