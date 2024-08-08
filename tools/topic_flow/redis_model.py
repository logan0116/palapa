import redis
import json


class RedisQueue:
    def __init__(self, name, maxsize, host='localhost', port=6379, db=0):
        self.__db = redis.Redis(host=host, port=port, db=db)
        self.name = name
        self.maxsize = maxsize

    def enqueue(self, id_, inputs, history):
        """ 将项目添加到队列，如果队列已满，则根据需要执行策略 """
        if self.size() <= self.maxsize:
            item = json.dumps({"id": id_, "inputs": inputs, "history": history})
            self.__db.rpush(self.name, item)
        else:
            raise Exception('RedisQueue is full')

    def dequeue(self):
        """ 从队列中移除并返回一个项目 """
        item = self.__db.lpop(self.name)
        return json.loads(item)

    def size(self):
        """ 返回队列中的项目数量 """
        return self.__db.llen(self.name)

    def clear(self):
        """ 清空队列 """
        self.__db.delete(self.name)


class RedisDict:
    def __init__(self, name, maxsize, host='localhost', port=6379, db=0):
        self.__db = redis.Redis(host=host, port=port, db=db)
        self.name = name
        self.maxsize = maxsize

    def set(self, key, value):
        """ 将键值对保存到字典中 """
        if self.size() <= self.maxsize:
            self.__db.hset(self.name, key, value)
        else:
            raise Exception('RedisDict is full')

    def get(self, key):
        """ 通过键获取值 """
        return self.__db.hget(self.name, key)

    def exists(self, key):
        """ 检查键是否存在于字典中 """
        return self.__db.hexists(self.name, key)

    def delete(self, key):
        """ 根据键删除键值对 """
        return self.__db.hdel(self.name, key)

    def size(self):
        """ 返回字典中的键值对数量 """
        return self.__db.hlen(self.name)

    def clear(self):
        """ 清空字典 """
        self.__db.delete(self.name)

    def get_keys(self):
        """ 返回字典中的键 """
        return [key.decode('utf-8') for key in self.__db.hkeys(self.name)]
