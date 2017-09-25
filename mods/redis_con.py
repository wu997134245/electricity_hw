# coding=utf-8

import redis
import pickle

class Redis():
    def __init__(self, host,port, password):
        pool = redis.ConnectionPool(host=host, port=port, password=password)
        self.r = redis.Redis(connection_pool=pool)


    def set(self,name,data):
        data = pickle.dumps(data)
        self.r.set(name,data,)


    def get(self,name):
        data = self.r.get(name)
        if not data:
            return {}
        return pickle.loads(data)

    def dele(self,name):
        status = self.r.delete(name)
        return status

    def hmset(self,name,data):
        data = pickle.dumps(data)
        self.r.hmset(name,data)

    def hmget(self,name):
        data = pickle.loads(self.r.hgetall(name))
        return data

r = Redis(host = '192.168.9.34', port= 6379, password = 'zq2014.')
print r.get('tom')
#print r.dele('tom')