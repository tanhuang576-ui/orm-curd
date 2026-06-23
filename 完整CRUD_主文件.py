"""
第二周产出：完整的图书 CRUD REST API
FastAPI + SQLAlchemy + SQLite + Pydantic 参数校验
运行命令：uvicorn 完整CRUD_主文件:app --reload
然后打开 http://127.0.0.1:8000/docs 测试所有接口
"""
from fastapi import FastAPI, Depends, HTTPException, Path, Query
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

# ========== 1. 数据库配置 ==========

# 数据库连接（SQLite，自动创建 book.db 文件，无需额外安装数据库）
DATABASE_URL = "sqlite:///./book.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal = 每个请求获取一个数据库会话的工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = 所有 ORM 模型继承它，用来建表
Base = declarative_base()

# ========== 2. ORM 模型（数据库表） ==========

class BookModel(Base):
    """books 表：存储图书数据"""
    __tablename__ = "books"

    id       = Column(Integer, primary_key=True, autoincrement=True, comment="图书ID")
    title    = Column(String(200), nullable=False, comment="书名")
    author   = Column(String(100), nullable=False, comment="作者")
    price    = Column(Float, nullable=False, comment="价格")
    category = Column(String(50), default="未分类", comment="分类")

# 启动时自动建表（如果表不存在则创建）
Base.metadata.create_all(bind=engine)

# ========== 3. Pydantic 校验模型（请求/响应） ==========

class BookCreate(BaseModel):
    """新增图书请求体"""
    title:    str  = Field(..., min_length=1, max_length=200, description="书名",
                           examples=["Python编程从入门到实践"])
    author:   str  = Field(..., min_length=1, max_length=100, description="作者")
    price:    float = Field(..., gt=0, le=99999, description="价格，必须大于0")
    category: str  = Field(default="未分类", max_length=50, description="分类")

class BookUpdate(BaseModel):
    """修改图书请求体（所有字段可选）"""
    title:    Optional[str]   = Field(None, min_length=1, max_length=200, description="书名")
    author:   Optional[str]   = Field(None, min_length=1, max_length=100, description="作者")
    price:    Optional[float] = Field(None, gt=0, le=99999, description="价格")
    category: Optional[str]   = Field(None, max_length=50, description="分类")

class BookResponse(BaseModel):
    """返回给前端的图书数据（隐藏了 ORM 内部细节）"""
    id:       int
    title:    str
    author:   str
    price:    float
    category: str

    class Config:
        from_attributes = True  # 允许从 ORM 对象自动转换

# ========== 4. 依赖注入：获取数据库会话 ==========

def get_db():
    """每个请求获取独立的数据库会话，请求结束后自动关闭"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ========== 5. FastAPI 应用实例 ==========

app = FastAPI(
    title       = "图书管理 CRUD API",
    description = "第二周产出：增删改查 + 参数校验 + 依赖注入",
    version     = "1.0.0"
)

# CORS 中间件（允许前端跨域调用）
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

# ========== 6. CRUD 接口 ==========

# ---------- C：新增图书 ----------
@app.post("/books", response_model=BookResponse, summary="新增图书")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    新增一本图书。
    - title 必填，1-200字符
    - author 必填，1-100字符
    - price 必填，>0 且 ≤99999
    - category 选填，默认"未分类"
    """
    new_book = BookModel(**book.model_dump())  # 把校验后的数据传入 ORM
    db.add(new_book)
    db.commit()
    db.refresh(new_book)  # 刷新拿到自增ID
    return new_book


# ---------- R：查询所有 ----------
@app.get("/books", response_model=list[BookResponse], summary="查询所有图书")
def list_books(
    page:     int = Query(default=1,  ge=1,           description="页码"),
    page_size: int = Query(default=10, ge=1, le=100,   description="每页数量"),
    keyword:  str = Query(default="",                  description="按书名模糊搜索"),
    db: Session = Depends(get_db)
):
    """分页查询图书，支持按书名模糊搜索"""
    query = db.query(BookModel)

    # 如果传了关键字，进行模糊匹配
    if keyword:
        query = query.filter(BookModel.title.contains(keyword))

    total = query.count()
    books = query.offset((page - 1) * page_size).limit(page_size).all()

    return books


# ---------- R：查询单本 ----------
@app.get("/books/{book_id}", response_model=BookResponse, summary="查询单本图书")
def get_book(
    book_id: int = Path(..., gt=0, description="图书ID"),
    db: Session = Depends(get_db)
):
    """根据ID查询图书，如果不存在则返回404"""
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"图书ID={book_id} 不存在")
    return book


# ---------- U：修改图书 ----------
@app.put("/books/{book_id}", response_model=BookResponse, summary="修改图书")
def update_book(
    book_id: int = Path(..., gt=0, description="图书ID"),
    data: BookUpdate = ...,  # ... 表示必传请求体
    db: Session = Depends(get_db)
):
    """支持部分修改：只传需要改的字段即可"""
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"图书ID={book_id} 不存在")

    # 只更新传了值的字段（exclude_unset=True）
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


# ---------- D：删除图书 ----------
@app.delete("/books/{book_id}", summary="删除图书")
def delete_book(
    book_id: int = Path(..., gt=0, description="图书ID"),
    db: Session = Depends(get_db)
):
    """根据ID删除图书，返回204表示成功"""
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"图书ID={book_id} 不存在")

    db.delete(book)
    db.commit()
    return {"message": f"图书ID={book_id} 已删除"}


# ========== 7. 启动入口 ==========
if __name__ == "__main__":
    import uvicorn, webbrowser, threading
    # 延迟1秒打开浏览器（等服务器启动）
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:8000/docs")).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
# uvicorn 完整CRUD_主文件:app --reload