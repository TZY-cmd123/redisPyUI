import redis

# HostAddress=str(input())
# Port=int(input())#输入测试
# 建立连接
HostAddress = "127.0.0.1"
Port = 6379
r = redis.Redis(host=HostAddress, port=Port, db=0)  # 指定0号数据库
# redis-py 使用 connection pool 来管理对一个 redis server 的所有连接，避免每次建立、释放连接的开销。
# 默认，每个Redis实例都会维护一个自己的连接池。
# 可以直接建立一个连接池，然后作为参数 Redis，这样就可以实现多个 Redis 实例共享一个连接池。
pool = redis.ConnectionPool(host=HostAddress, port=Port, decode_responses=True)
r = redis.Redis(connection_pool=pool)
r1 = redis.StrictRedis(host=HostAddress, port=Port)  # 这是主要的redis方法，redis.Redis是它的子类

# 数据库基础操作
# 查看所有键值
print(r.keys())  # 所有键
# 查看所有键
for i in r.keys():
    print(r.type(i))  # 获得键值的类型
    r.expire(i, 10)  # 设置过期时间
    print(r.ttl(i))  # 获得过期时间
    r.rename(i, 'hello' + i)  # 重命名
    r.move(i, 1)  # 转移到指定数据库
    r.delete(i)  # 根据键删除键值对
r.flushdb()  # 删除当前数据库
r.flushall()  # 删除所有数据库

# 普通键值对操作
##set key/value
r.set(1, 2)  # ex是过期时间
r.set("12", "Hello")
# get key
print(r.get(1))
r.incr(1, 20)  # 对key1自增20
r.incrbyfloat(1, 20.1)  # 自增浮点型数据
# r.decr(1,1)#自减操作,这里如果这么写会有bug，是因为被转化成字符串型
r.append("12", "World")  # 对字符型value增加

# list类型操作
r.rpush('list1', 1, 2, 32, 3, 4)  # 插入列表，可以在表尾插入多个元素
r.lpush('list1', 1, 2, 32, 3, 4)  # 插入列表，可以在表头插入多个元素
r.lset('list1', 1, 100)  # 设置值
r.lrem('list1', num=1, value=2)  # 删除1个值为2
listRedis = r.lrange('list1', 0, -1)  # 根据范围获得列表
print(listRedis)

# set类型
r.sadd("set1", 1, 2, 3, 4)  # 往集合里增加元素
r.sadd("set2", 2, 3, 5)  # 往集合里增加元素
setRedis = r.smembers('set1')  # 获得所有元素
print(setRedis)
r.srem('set1', 1)  # 删除值为1的元素
r.smove('set1', 'dst', 2)  # 把2从第一个集合移动到第二个集合
diffset = r.sdiff('set1', 'set2')  # 求差集
print(diffset)
interset = r.sinter('set1', 'set2')  # 求交集
print(interset)
unionset = r.sunion('set1', 'set2')  # 求并集
print(unionset)

# zset比set多了一个元素权值的选项

# hash数据操作,hash类似与dict
r.hset("hash1", "k1", "v1")
r.hset("hash1", "k2", "v2")  # 添加hash散列

print(r.hkeys("hash1"))  # 取hash中所有的key
print(r.hvals('hash1'))  # 获得所有value
print(r.hget("hash1", "k1"))  # 单个取hash的key对应的值
hashdict=r.hgetall('hash1')#获得该hash表
print(hashdict)

r.hdel("hash1", "k1")    # 删除一个键值对
r.hincrby("hash1", 'k1', amount=1)  # 自增

