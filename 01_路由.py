#路由是URL地址和处理函数之间的映射关系
from idlelib.colorizer import matched_named_groups

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}


# 访问/hello 响应结果：msg：你好 FASTAPI

# @app.get("/hello")
#
# async def get_hello():
#     return {'msg':'你好 FASTAPI'}
#
# @app.get('/user/hello')
#
# async def get_res():
#     return {'msg':'我正在学习路由'}
# uvicorn 01_路由:app --reload



@app.get("/book")

async def get_book(book):
    return {"book":book}