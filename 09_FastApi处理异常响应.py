#路由是URL地址和处理函数之间的映射关系
from importlib import reload

from fastapi import FastAPI
from fastapi import HTTPException #异常响应处理导这个包

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}


# #需求：按id查询新闻 -> 1-6
# @app.get("/news/{id}")
# async def get_news(id:int):
#     id_list = [1,2,3,4,5,6]
#     if id not in id_list:
#         raise HTTPException(status_code=404, detail="您查找的新闻不存在") #status_code 是状态码 必须填
#
#     return {"id":id}



@app.get("/news/get_id")

# id_list=[1,2,3,4,5,6]
async def get_id_name(
    id:int,
    name:str):

    id_list = [1, 2, 3, 4, 5, 6]
    err=[]
    name_list=["张三","李四","王五"]
    if id not in id_list:
        err.append("您查找的新闻不存在")
    if name not in name_list:
        err.append("抱歉，您不是我们的用户")
    if err:
        raise HTTPException(status_code=404,detail=err)


    return {"id":id,"name":name}

# uvicorn 09_FastApi处理异常响应:app --reload