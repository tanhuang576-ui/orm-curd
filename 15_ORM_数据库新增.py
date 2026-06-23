# 新增：
# 核心步骤：
# 定义ORM对象 -> 添加对象到事务：add(对象) -> commit 提交到数据库
# 用户输入  -> 参数 -> 请求体

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
    ASYNC_DATABASE_URL,#数据库信息
    echo=True,#可选输出sql日志
    pool_size=10,#设置连接池活跃的连接数
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