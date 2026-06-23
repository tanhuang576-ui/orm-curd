import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import DateTime, String, Float, func
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 生命周期
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await async_engine.dispose()

app = FastAPI(lifespan=lifespan)

# 数据库连接
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/itheima?charset=utf8"
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True, pool_size=10, max_overflow=20)

class Base(DeclarativeBase):
    create_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        comment='创建时间'
    )
    update_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment='修改时间'
    )

class Book(Base):
    __tablename__ = 'book'
    id: Mapped[int] = mapped_column(primary_key=True, comment='书籍id')
    bookname: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="书籍价格")
    publisher: Mapped[str] = mapped_column(String(255), comment='出版社')

# 建表
async def create_tables():
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "helloworld"}

# uvicorn 12_ORM_创建数据库引擎:app --reload