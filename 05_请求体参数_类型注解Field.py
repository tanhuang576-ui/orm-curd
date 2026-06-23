#  uvicorn 05_请求体参数_类型注解Field:app --reload
from symtable import Class

from fastapi import FastAPI
from pydantic import  BaseModel,Field
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}



#注册：用户名和密码 -》str
# 请求体参数：先定义类型 然后再进行类型注解
class User(BaseModel):
    username: str = Field(default="张三",min_length=2,max_length=10,description="用户名，长度有要求：2-10个字符")
    password: str = Field(...,min_length=3,max_length=20)


# 写路由
@app.post("/register")
async def register(user: User):
    # user:形参 类型是：class User
    return user


# 请求体参数作用：创建，更新资源
# 如何定义，使用请求体参数？
# 从Pydantic中导入 BaseModel
# 给请求体参数做类型注解：python原生 和 Field注解



# from fastapi import  FastAPI
# from pydantic import BaseModel,Field
#
# app = FastAPI()
#
#
# class User(BaseModel):
#     name:str = Field(default="张三",min_length=1,max_length=6,description="name的长度限制")
#     password:int=Field(default="",min_length=4,max_length=20,description="密码长度限制")
#
# @app.post("/register")
#
# async def get_user(user:User):
#     return user
# uvicorn 05_请求体参数_类型注解Field:app --reload