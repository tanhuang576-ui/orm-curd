# 中间件是一个在每次进入FastApi应用时都会被执行的函数
# 它在请求到达实际的路径操作之前运行 并且在响应返回给客户端之前再运行一次
# 中间件作用是为每一个请求添加统一的处理逻辑
# 中间件的定义：函数顶部使用装饰器@app.middleware("http")
# 多个中间件的执行顺序时自下而上

# 执行顺序：请求-》外层中间件-》print(中间件2 start) -》call_next(request)交给内层中间件1
# 进中间件1-》print(中间件1 start) -> call_next交给接口
# 接口执行完毕 反向原路返回
# 中间件1剩余代码：print(中间件1 end),返回响应
# 回到中间键2剩余代码：print(中间件2 end),返回响应

from fastapi import FastAPI,Path

app=FastAPI()

@app.middleware("http")
async def middleware1(request,call_next):#参数必有一个请求和一个传递请求的函数名 官方文档里固定的是call_next()
    print("中间件1 start")
    response =  await call_next(request) #这里是把响应交给接口了
    print("中间件1 end")
    return response


@app.middleware("http")
async def middleware2(request,call_next):#参数必有一个请求和一个传递请求的 官方文档里固定的是call_next()
    print("中间件2 start")
    response =  await call_next(request)
    print("中间件2 end")
    return response



@app.get("/")
async def root():
    return {"message":"hello world"}
# uvicorn 10_中间件:app --reload