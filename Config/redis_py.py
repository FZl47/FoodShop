import redis
import pickle

REDIS_CONFIG = {
    'host':'localhost',
    'port':'6379'
}

REDIS = redis.Redis(**REDIS_CONFIG)

def pack_data(data):
    return pickle.dumps(data)

def unpack_data(data):
    return pickle.loads(data)

def add_to_list(key,data):
    data = pack_data(data)
    REDIS.lpush(key,data)
    return True

def get_list(key):
    data = REDIS.lrange(key,0,-1)
    return data

def get_list_upacked(key):
    return [unpack_data(data) for data in get_list(key)]

def get_len_list(key):
    return REDIS.llen(key)

def remove_first_element_list(key):
    REDIS.lrem(key,1,REDIS.lindex(key,-1))
    return True

def set_value(key,value):
    REDIS.set(key,pack_data(value))
    return True

def set_value_expire(key,value,seconds):
    REDIS.set(key,pack_data(value),ex=seconds)
    return True

def get_value(key):
    data = REDIS.get(key)
    if data:
        return unpack_data(data)
    return None

def remove_key(key):
    REDIS.delete(key)
    return True

def clear_db():
    REDIS.flushdb()
    return True

