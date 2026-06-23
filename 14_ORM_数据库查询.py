# 核心语句：
# x = await db.execute select((模型类)),返回一个ORM对象
#
# 获取所有数据：
# x.scalars().all
#
# 获取单条数据：
# x.scalars().first 获取第一条数据
# x.get(模型类，主键值) 获取单条数据 -> 根据主键获取

#条件查询
# 语法：
# select(Book).where(条件1，条件2，....)
#
# 查询条件：
# 比较判断：==；>;<;<=;>=
# 模糊查询：like()
# %：匹配零个 一个或多个字符

# _:匹配一个单个字符
# 与或非查询：与：&；或者：|;非：~
# 包含查询：in_()
#
# 聚合查询：
# 聚合计算：func.方法（模型类.属性）
# count:统计行数
# db.execute(select(func.count(模型类.属性)))
# avg:计算平均值
# db.execute(select(func.avg(模型类.属性)))
# max：求最大值
# db.execute(select(func.max(模型类.属性)))
# min:求最小值
# db.execute(select(func.min(模型类.属性)))
# sum:求和
# db.execute(select(func.sum(模型类.属性)))
# 返回的值如果用result接收：
# result = await db.execute(select(func.count(模型类.属性)))
# num = result.scalar() #用来提取一个数值 -> 标量值

# 分页查询：
# 语法：
# select().offset().limit
# offset:跳过的记录数
# limit:返回的记录数

# offset值 = （当前页码-1）*每页数量limit


# 从ORM对象获取数据的方式
# 1.获取所有数据
# scalars().all
# 2.获取单条数据
# scalars().first():提取第一个数据
# scalar_one_or_none():提取一个或null
# scalar():提取标量值（配合聚合查询使用）


