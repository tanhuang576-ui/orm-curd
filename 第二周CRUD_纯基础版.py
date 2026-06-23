"""
第二周产出：图书 CRUD REST API（纯基础版）
用到的知识：路由 + 路径参数 + 查询参数 + 请求体 + Pydantic + 异常处理 + 依赖注入

运行：uvicorn 第二周CRUD_纯基础版:app --reload
然后打开 http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI, Depends, HTTPException, Path, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="图书管理 CRUD（第二周基础版）")

# ========== 1. 用列表模拟数据库（没有 SQL，没有 ORM）==========
# 这是本周该用的方式——你还没学数据库，用内存存储就够了
books_db: list[dict] = [
    {"id": 1, "title": "活着",   "author": "余华",  "price": 29.9},
    {"id": 2, "title": "三体",   "author": "刘慈欣", "price": 68.0},
    {"id": 3, "title": "围城",   "author": "钱锺书", "price": 36.0},
]
next_id = 4  # 自增ID


# ========== 2. Pydantic 请求体模型（数据校验）==========

class BookCreate(BaseModel):
    """新增/修改时用的模型"""
    title:  str   # 只做类型校验，不加花哨的 Field
    author: str
    price:  float


# ========== 3. 依赖注入（本周学的内容之一）==========

def get_book_or_404(book_id: int = Path(...)):
    """通用的"按ID找书，找不到就404"——这就是依赖注入的实际用法"""
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail=f"图书ID={book_id} 不存在")


# ========== 4. CRUD 接口 ==========

# C —— 增
@app.post("/books", summary="新增图书")
def create_book(data: BookCreate):
    global next_id
    new_book = {"id": next_id, "title": data.title, "author": data.author, "price": data.price}
    books_db.append(new_book)
    next_id += 1
    return new_book


# R —— 查全部
@app.get("/books", summary="查询所有图书")
def list_books(
    keyword: str = Query(default="", description="按书名模糊搜索"),
    min_price: Optional[float] = Query(default=None, description="最低价格"),
):
    result = books_db
    if keyword:
        result = [b for b in result if keyword in b["title"]]
    if min_price is not None:
        result = [b for b in result if b["price"] >= min_price]
    return result


# R —— 查单本（用依赖注入找书）
@app.get("/books/{book_id}", summary="查询单本图书")
def get_book(book: dict = Depends(get_book_or_404)):
    return book


# U —— 改
@app.put("/books/{book_id}", summary="修改图书")
def update_book(data: BookCreate, book: dict = Depends(get_book_or_404)):
    book["title"]  = data.title
    book["author"] = data.author
    book["price"]  = data.price
    return book


# D —— 删
@app.delete("/books/{book_id}", summary="删除图书")
def delete_book(book: dict = Depends(get_book_or_404)):
    books_db.remove(book)
    return {"message": f"图书《{book['title']}》已删除"}
# uvicorn 第二周CRUD_纯基础版:app --reload