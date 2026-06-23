from contextlib import asynccontextmanager
from dataclasses import field
from datetime import datetime
from fastapi import FastAPI, Depends
from sqlalchemy import DateTime, String, Float, func, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel

# ========== 创建数据库配置和引擎 ==========
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/itheima?charset=utf8"
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,#告诉 SQLAlchemy 使用哪种数据库（MySQL）、异步驱动（aiomysql）、认证信息、主机、端口和数据库名。
    echo=True,#相当于开启 SQL 日志记录。每个通过引擎执行的 SQL 语句都会打印到控制台。
              # 开发阶段建议设为 True，方便排查问题；生产环境通常设为 False 减少性能开销。
    pool_size=10,#连接池维持的常驻连接数。即使这些连接空闲，也会保持打开状态。
    max_overflow=20 #允许额外的连接数
)
# ========== 创建基类和模型 ==========
class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        comment='创建时间'
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment='修改时间'
    )


    # 定义表
class Book(Base):
    __tablename__ = 'book'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,comment='id')
    bookname: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="书籍价格")
    publisher: Mapped[str] = mapped_column(String(255),nullable=True, comment='出版社')

# ========== 建表函数 ==========
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ========== 生命周期管理 ==========
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建表
    await create_tables()
    print("数据库表已创建/检查完成")
    yield
    # 关闭时释放引擎连接池
    await async_engine.dispose()
    print("数据库连接池已释放")

# ========== FastAPI 应用实例 ==========
app = FastAPI(lifespan=lifespan)

#需求：查询功能的接口，查询图书 -> 依赖注入：创建依赖项获取数据库会话 + Depends 注入路由处理函数
# ==========创建异步会话工厂 ==========
AsyncSessionLocal = async_sessionmaker(

    bind=async_engine, #绑定数据库引擎
    class_=AsyncSession, #指定会话类
    expire_on_commit=False #提交后会话不过期，不会重新查询数据库
)
# ========== 依赖项：获取数据库会话 ==========
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
          yield session #返回数据库会话给路由处理函数
          await session.commit() #无异常，提交
        except Exception:
          await session.rollback()#有异常 回滚
          raise
        finally:
            await session.close()#关闭会话


# ========== 8. 示例路由（使用数据库） ==========
@app.get("/")
async def root():
    return {"message": "helloworld"}

# @app.get("/book/books")
# async def get_books(db: AsyncSession = Depends(get_db)):  #db:AsyncSession 给db赋值为这个类型
#     #查询
#     result = await db.execute(select(Book))
#     books = result.scalars().all() #查询所有图书
#     return books
# uvicorn 13_路由匹配中使用ORM:app --reload


# 需求：路径参数 书籍id
@app.get("/book/get_book/{book_id}")
async def get_book_list(book_id:int,db:AsyncSession = Depends(get_db)):
    result=await db.execute(select(Book).where(Book.id==book_id))
    book=result.scalar_one_or_none()
    return book

#模糊查询
# %：零个 一个或多个字符
# _:一个或单个字符

#查找作者以“曹”卡头的
# @app.get("/book/search_book")
# async def get_search_book(db:AsyncSession=Depends(get_db)):
#
#     res1=await db.execute(select(Book).where(Book.author.like("曹%")))
#     res1 = await db.execute(select(Book).where((Book.author.like("曹%")) & (Book.price>100)))
#
#     #需求：书籍id列表 数据库里面的id如果再书籍id列表里面 就返回
#     id_list=[1,3,5,7]
#     res1 = await db.execute(select(Book).where(Book.id.in_(id_list)))
#     book=res1.scalars().all()
#     return book
#
# @app.get("/book/get_book_list")
# async def get_book_list(
#         page:int=1,
#         page_size:int=6,
#         db:AsyncSessionLocal=Depends(get_db)

# ):
#     #offset:跳过的记录数 limit:每页的记录数
   # res1= select(Book).offset((page-1)*page_size).limit(page_size)
   # res2 = await db.execute(res1)
   # books=res2.scalars().all()
   # return books

# 需求：用户输入图书信息（id,书名，作者，价格，出版社） -> 新增
# 用户输入 -> 参数 -> 请求体
class BookCreate(BaseModel):
    id:int
    bookname:str
    author:str
    price:float
    publisher:str




@app.post("/book/add_book")
async def add_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    # 直接使用 book.dict() 或 book.model_dump()（Pydantic v2）
    book_obj = Book(**book.__dict__) #转为orm类 方便后续进行增加操作
    db.add(book_obj)
    await db.commit()
    await db.refresh(book_obj)   # 刷新获取自增 id
    return book_obj