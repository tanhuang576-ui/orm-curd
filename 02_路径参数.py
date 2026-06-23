from fastapi import FastAPI,Path

app=FastAPI()



@app.get("/")
async def root():
    return {"message":"hello world"}


 # uvicorn 路径参数:app --reload

@app.get("/book/{id}")
# 路径参数 底下定义的函数路径里要有同名形参

#path注解可以给路径参数添加类型注解

async def get_book(id:int = Path(..., gt=0,lt=101,description="书籍id,取值范围：1-100之间")):
    #path方法里的 gt表示大于 ge是大于等于 lt是小于 le是小于等于
    return {"id":id,"title":f"这是第{id}本书"}


#需求：查找书籍的作者，路径参数 name ,长度范围 2-10

# @app.get("/author/{name}")
# async def get_name(name:str=Path(...,min_length=2,max_length=10,description="作者名字长度取值范围在2-10之间")):
#     return {"msg":f"这是{name}得信息"}
#
# @app.get("/news/{id}")
# async def get_news(id:str = Path(...,gt=0,lt=101,description="id范围是1-100")):
#     return {"id":id,"title":f"这是{id}的id"}
#
# @app.get("/classify/{name}")
# async def get_news(name:str = Path(...,min_length=1,max_length=100,description="id范围是1-100")):
#     return {"id":id,"title":f"这是{name}的id"}








@app.get("/author/{name}")

async def get_name(name=Path(...,min_length=1,max_length=6,description="name的范围是1-6")):
    return {"name":name,"title":f"这是{name}的名字"}
# uvicorn 02_路径参数:app --reload



