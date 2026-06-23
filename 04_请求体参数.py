# 在http协议中 一个完整的请求由三部分组成：
# 1.请求行：包含方法，url,协议版本
# 2.请求头：元数据信息
# 3.请求体：实际要发送的数据内容

from fastapi import FastAPI
from pydantic import  BaseModel
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}



#注册：用户名和密码 -》str
# 请求体参数：先定义类型 然后再进行类型注解
class User(BaseModel):
    username: str
    password: str


# 写路由
@app.post("/register")
async def register(user: User):
    # user:形参 类型是：class User
    return user
# # uvicorn 04_请求体参数:app --reload
#
# class Book(BaseModel):
#      book_name:str
#      author:str
#      press:str
#      price:float
#
# @app.post("book_seek")
# async def book_seek(message:Book):
#     return message



# from fastapi import FastAPI
# from pydantic import BaseModel
#
# app=FastAPI()
#
# class User(BaseModel):
#     name:str
#     id:int
#
# @app.post("/register")
#
# async def get_user(user:User):
#     return user
