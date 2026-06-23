from contextlib import asynccontextmanager

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped,mapped_column
from datetime import datetime
from sqlalchemy import DateTime,func,String,Float,Integer,select
import os
from fastapi import FastAPI,Depends,HTTPException


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield
    await async_engine.dispose()

app = FastAPI(lifespan=lifespan)


ASYNC_DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://root:123456@localhost:3306/sys?charset=utf8")
#创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)

#创建基类
class Base(DeclarativeBase):
    create_time:Mapped[datetime]=mapped_column(
        DateTime,
        server_default=func.now(),
        comment='创建时间'

    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment='结束时间'

    )

# 定义一个学生表
class Student(Base):
    __tablename__ = 'student'
    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True,comment="学生id")
    name:Mapped[str]=mapped_column(String(255),comment="学生姓名")
    gender:Mapped[str]=mapped_column(String(10),comment="学生性别")
    age:Mapped[int]=mapped_column(Integer,comment="学生年龄")
    major:Mapped[str]=mapped_column(String(20),comment="主修课程")

#创表
async def create_table():
    async with async_engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)


#创建异步会话工厂

AsyncSessionLocal=async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=True

)


#获取数据库

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

@app.get("/")
async def get_root():
    return {"Hello":"World"}


class StudentCreate(BaseModel):
    name: str
    gender: str
    age: int
    major: str

#增添学生数据
@app.post("/student/create_student")
async def create_student(
        student:StudentCreate,db:AsyncSession=Depends(get_db)

):
    student_ojc=Student(**student.model_dump())
    db.add(student_ojc)
    await db.commit()
    await db.refresh(student_ojc)
    return student_ojc

#查询学生数据
# 查询所有学生



@app.get("/student/get_student/{get_id}")
async def get_student(
       get_id:int, db:AsyncSession=Depends(get_db)
):
   result=await db.execute(select(Student).where(Student.id==get_id))
   student=result.scalar_one_or_none()
   return student

@app.get("/student/list_all")
async def list_all_student(db: AsyncSession = Depends(get_db)):
    # 查询全部学生
    stmt = select(Student)
    result = await db.execute(stmt)
    student_list = result.scalars().all()
    return student_list
#更改学生数据

class UpDate(BaseModel):
    name: str
    gender: str
    age: int
    major: str


@app.put("/student/update_student/{student_id}")
async def put_student(student_id:int,update:UpDate, db:AsyncSession=Depends(get_db)):
    db_student=await db.get(Student,student_id)
    if db_student is None:
        raise HTTPException(status_code=404,detail="查无此人")
    db_student.name=update.name
    db_student.gender=update.gender
    db_student.age=update.age
    db_student.major=update.major
    await db.commit()


@app.delete("/student/delete_student/{student_id}")
async def delete_student(student_id:int, db:AsyncSession=Depends(get_db)):
    db_student=await db.get(Student,student_id)
    if db_student is None:
        raise HTTPException(status_code=404,detail="查无此人")
    await db.delete(db_student)
    await db.commit()
    return {"msg":"删除学生成功"}








# uvicorn ORM_CRUD:app --reload










