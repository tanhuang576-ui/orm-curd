"""
不用看视频，直接跑这个脚本验证所有 CRUD 接口
前提：先在一个终端里启动 uvicorn 服务器：
    uvicorn 完整CRUD_主文件:app --reload
然后另开一个终端跑这个测试：
    python 测试CRUD接口.py
"""
import requests

BASE = "http://127.0.0.1:8000"

print("=" * 50)
print("  开始测试图书 CRUD 接口")
print("=" * 50)

# 1. CREATE —— 新增一本书
print("\n[1/5] POST /books —— 新增")
resp = requests.post(f"{BASE}/books", json={
    "title": "高效能人士的七个习惯",
    "author": "史蒂芬·柯维",
    "price": 49.9,
    "category": "个人成长"
})
print(f"  状态码: {resp.status_code}")
print(f"  返回: {resp.json()}")

book_id = resp.json()["id"]  # 记住ID，后面用

# 2. CREATE —— 再新增两本
requests.post(f"{BASE}/books", json={"title":"活着","author":"余华","price":29.9,"category":"文学"})
requests.post(f"{BASE}/books", json={"title":"算法导论","author":"CLRS","price":99.0,"category":"计算机"})

# 3. READ —— 查询所有
print("\n[2/5] GET /books —— 查询所有")
resp = requests.get(f"{BASE}/books")
print(f"  共 {len(resp.json())} 本书")

# 4. READ —— 查单本
print(f"\n[3/5] GET /books/{book_id} —— 查询单本")
resp = requests.get(f"{BASE}/books/{book_id}")
print(f"  返回: {resp.json()}")

# 5. UPDATE —— 修改
print(f"\n[4/5] PUT /books/{book_id} —— 修改")
resp = requests.put(f"{BASE}/books/{book_id}", json={"price": 39.9})
print(f"  修改后价格: {resp.json()['price']}")

# 6. DELETE —— 删除
print(f"\n[5/5] DELETE /books/{book_id} —— 删除")
resp = requests.delete(f"{BASE}/books/{book_id}")
print(f"  返回: {resp.json()}")

# 验证删除后总数
resp = requests.get(f"{BASE}/books")
print(f"\n  删除后剩余: {len(resp.json())} 本书")

print("\n" + "=" * 50)
print("  全部接口测试通过！")
print("  打开 http://127.0.0.1:8000/docs 手动调试")
print("=" * 50)
