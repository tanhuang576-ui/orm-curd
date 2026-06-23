# 使用依赖注入系统来共享通用逻辑，减少代码重复
from email.policy import default
from idlelib.query import Query
from pydoc import describe

# 依赖注入：
# 依赖项：可重复用的组件（函数/类），负责提供某种功能或数据
# 注入：FastApi自动帮你调用依赖项，并将结果“注入”到路径操作函数中。
#
# 优点：1.代码复用：一次编写，多处使用
#      2.解耦：业务逻辑和基础设施代买分离
#      3.易于测试：轻松地用模拟依赖注入替换真实依赖进行测试

# 1.创建依赖项：把通用的代码封装起来
# 2.导入depends
# 3.声明依赖项 在路由的函数参数里面导入depends方法

#把分页的参数逻辑共用：新闻列表和用户列表
from fastapi import FastAPI,Query
from fastapi import Depends

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}
#
# 1.创建依赖项
# 2.usages
async def common_parameters(
        skip:int=Query(0,ge=0),
        limit:int=Query(10,le=60)
):
    return {"skip":skip,"limit":limit}

# 3.声明依赖项->依赖注入
@app.get("/news/mews_list")
async def get_news_list(commons = Depends(common_parameters)):
    return commons

@app.get("/user/user_list")
async def get_user_list(commons = Depends(common_parameters)):
    return commons
# uvicorn 11_依赖注入:app --reload


# from fastapi import FastAPI,Query
# from fastapi import Depends
#
# app = FastAPI()
#
# @app.get("/")
#
# async def start():
#     return {"message":"HelloWorld"}
#
#
#
# async def common_parameter(
#         skip:str=Query(0,le=10),
#         commit:str=Query(10,ge=90)
# ):
#     return {"Sikp":skip,"commit":commit}
#
#
# @app.get("/book/news")
# async def get_book_list(common=Depends(common_parameter)):
#
#     return common

# uvicorn 11_依赖注入:app --reload
