#中间件只要执行 就会在全局接口生效

from fastapi import FastAPI, Request
import time
app = FastAPI()

@app.middleware("http")
async def demo_middle(request:Request,call_next):
    # ===== 请求进来：接口执行前 =====
    start = time.time()
    # 放行，执行接口函数
    resp = await call_next(request)
    # ===== 接口跑完，返回响应前 =====
    cost = time.time()-start
    print(f"接口耗时：{cost:.2f}s")
    return resp


@app.get("/test")
async def test():
    return "这是测试接口"

 # uvicorn 1:app --reload