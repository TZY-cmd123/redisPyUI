import redis
# HostAddress=str(input())
# Port=int(input())#输入测试
#建立连接
HostAddress="127.0.0.1"
Port=6379
r = redis.Redis(host=HostAddress, port=Port, db=0)
# redis-py 使用 connection pool 来管理对一个 redis server 的所有连接，避免每次建立、释放连接的开销。
# 默认，每个Redis实例都会维护一个自己的连接池。
# 可以直接建立一个连接池，然后作为参数 Redis，这样就可以实现多个 Redis 实例共享一个连接池。
pool = redis.ConnectionPool(host=HostAddress, port=Port, decode_responses=True)
r = redis.Redis(connection_pool=pool)


#普通键值对操作
##set key/value
r.set(1,2,ex=3)#ex是过期时间
r.set("12","Hello")
#get key
print(r.get(1))
r.incr(1,20)#对key1自增20
r.incrbyfloat(1,20.1)#自增浮点型数据
#r.decr(1,1)#自减操作,这里如果这么写会有bug，是因为被转化成字符串型
r.append("12","World")#对字符型value增加
#查看所有键值
print(r.keys())#所有键
#查看所有键
for i in r.keys():
    print(r.get(i))#这个只能针对普通的键值对


#hash数据操作
r.hset("hash1", "k1", "v1")
r.hset("hash1", "k2", "v2")
r.hset("hash1", "k1", "v2")

print(r.hkeys("hash1")) # 取hash中所有的key
print(r.hget("hash1", "k1"))    # 单个取hash的key对应的值
#hash类似于字典


#list数据操作


