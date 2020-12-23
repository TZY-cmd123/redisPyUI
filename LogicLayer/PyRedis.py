import redis
# HostAddress=str(input())
# Port=int(input())#输入测试
HostAddress="127.0.0.1"
Port=6379
r = redis.Redis(host=HostAddress, port=Port, db=0)
# redis-py 使用 connection pool 来管理对一个 redis server 的所有连接，避免每次建立、释放连接的开销。
# 默认，每个Redis实例都会维护一个自己的连接池。
# 可以直接建立一个连接池，然后作为参数 Redis，这样就可以实现多个 Redis 实例共享一个连接池。
pool = redis.ConnectionPool(host=HostAddress, port=Port, decode_responses=True)
r = redis.Redis(connection_pool=pool)
#set key/value
r.set(1,2,ex=3)#ex是过期时间
#get key
print(r.get(1))
