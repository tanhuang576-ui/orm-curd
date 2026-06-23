# fastapi中默认的响应类是json
# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse
#
# app=FastAPI()
#
#
# @app.get("/")
# async def root():
#     return {"message":"Hello World"}
#
# #接口： -》响应HTML代码
# # 1.在fastapi中导入HTMLREsponse
# # 2.在装饰器请求路径后 加入resopnse_class=响应路径即可
#
# @app.get("/html",response_class=HTMLResponse)
#
# async def get_html():
#     return "<h1>这是一级标题</h1>"
# uvicorn 06_在装饰器中指定响应类:app --reload









from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app=FastAPI()

@app.get("/html",response_class=HTMLResponse)
async def get_html():
    return "<h1>这是一级标题<h1>"






