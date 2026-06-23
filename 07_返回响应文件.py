from fastapi import FastAPI
from fastapi.responses import FileResponse
app = FastAPI()

@app.get("/")
async def root():
    return {"message":"HelloWorld"}


#接口：返回一张图片内容
@app.get("/file")
async def get_file():
    path = "./imgs/image1.jpeg"
    return FileResponse(path)
# uvicorn 07_返回响应文件:app --reload


# FileResponse 是fast.api提供的专门用于返回文件内容
# （如：图片，PDF，EXCel，音视频等）的响应类。
# 他能够智能处理文件路径 媒体类型推断 范围请求和缓存头部是服务静态文件的推荐方式

# @app.get("/html",response_class=HTMLResponse)
#
# async def get_html():
#     return "<h1>这是一级标题</h1>"



#
# from fastapi import FastAPI
# from fastapi.responses import FileResponse
#
# app=FastAPI()



@app.get("/image")

async def get_image():
    path = "./imgs/image1.jpeg" #注意前面要加.
    return FileResponse(path)


