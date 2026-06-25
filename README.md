# 学生管理系统 API

基于 **FastAPI + SQLAlchemy + MySQL** 的 RESTful 学生管理接口，Docker 容器化部署。

## 🚀 在线地址

```
https://orm-curd.up.railway.app
```

在线文档（Swagger）：https://orm-curd.up.railway.app/docs

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| FastAPI | Web 框架 |
| SQLAlchemy 2.0 | ORM（异步） |
| MySQL + aiomysql | 数据库 |
| Pydantic | 数据校验 |
| Docker | 容器化 |
| Railway | 在线部署 |

## 📋 接口列表

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 根路由，返回 Hello World |
| POST | `/student/create_student` | 新增学生 |
| GET | `/student/get_student/{get_id}` | 根据 ID 查询学生 |
| GET | `/student/list_all` | 查询所有学生 |
| PUT | `/student/update_student/{student_id}` | 更新学生信息 |
| DELETE | `/student/delete_student/{student_id}` | 删除学生 |

## 📦 本地运行

### 1. 克隆代码

```bash
git clone https://github.com/tanhuang576-ui/orm-curd.git
cd orm-curd
```

### 2. 用 Docker 启动

```bash
# 先确认本机有 MySQL 在 3306 端口运行
docker build -t orm-crud:v1.0 .
docker run -d -p 8000:8000 \
  -e DATABASE_URL="mysql+aiomysql://root:你的密码@host.docker.internal:3306/sys?charset=utf8" \
  --name orm-api \
  orm-crud:v1.0
```

### 3. 访问

浏览器打开 `http://localhost:8000/docs`

## 📁 项目结构

```
.
├── ORM_CRUD.py          # 主程序
├── requirements.txt     # Python 依赖
├── Dockerfile           # Docker 构建文件
└── README.md            # 本文件
```

## 📝 示例请求

创建学生：

```bash
curl -X POST https://orm-curd.up.railway.app/student/create_student \
  -H "Content-Type: application/json" \
  -d '{"name": "张三", "gender": "男", "age": 20, "major": "计算机科学"}'
```

查询所有学生：

```bash
curl https://orm-curd.up.railway.app/student/list_all
```
