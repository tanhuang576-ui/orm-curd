#response_model 是路径操作装饰器（如@app.get 或者 @app.post)的关键参数 ，它通过一个Pydantic模型来严格定义和约束API端点的输出格式。
#这一机制在提供自动数据验证和序列化的同时 更是保障数据安全性的第一道防线
from os import name

#路由是URL地址和处理函数之间的映射关系
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}


#需求：新闻接口 -> 响应数据格式 id title content
# class News(BaseModel):
#     id:int
#     title:str
#     content:str
#
# @app.get("/news/{id}",response_model=News)
#
# async def get_news(id:int):
#
#     return {"id":id,
#             "title":f"这是第{id}本书",
#             "content":"这是一本好书"

            # uvicorn 08_自定义响应数据格式: app --reload
    # }
#约定了一个类型 就得完全遵守这个类型



class Book(BaseModel):
    name:str
    id:int
    author:str

@app.get("/book/{author}",response_model=Book)
async def get_book(id:int):
    return {
        "id":id,
        "name":f'这是一本第{id}本书',
        "author":'Nia'
    }

# uvicorn 08_自定义响应数据格式:app --reload