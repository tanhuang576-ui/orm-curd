#查询参数用处：筛选，分页，模糊搜索，附加参数
from fastapi import FastAPI,Query

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}


#需求 查询新闻 -》分页，skip：跳过的记录数，limit：返回的记录数 10
# 会自动识别查询参数
@app.get("/news/news_list")
async def get_news_list(
        skip:int = Query(0,description="跳过的记录数",lt=100),
        # 用query进行类型注解
        limit:int = Query(10,description="返回的记录数")
):
    return {"skip":skip,"limit":limit}

# 注意：查询参数出现在url？之后，k1 = v1 & k2 = v2
# 如何给查询参数加类型注解？
# Python原生注解 和 Query注解

#
# @app.get("/author/name")
#
# async def get_name(
#     skip:str = Query(...,gt=0,le=10,description="最小长度0，最大为10"),
#     page:str = Query(...,min_length=1,max_length=10)):
#     return {"跳过的页面数":skip,"跳过的界面":page}
# # uvicorn 03_查询参数:app --reload













