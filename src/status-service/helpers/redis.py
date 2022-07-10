import redis
import time

class RedisHelper():
  __instance = None

  def __init__(self):
    raise RuntimeError('Call instance() instead')
  
  @classmethod
  def instance(self, redis_host=None, redis_port=None, redis_password=None):
    if self.__instance is None:
      self.__instance = self.__new__(self)
      while True:
        try:
          self.connection = redis.Redis(host=redis_host, port=redis_port, db=0, password=redis_password)
          self.expire_time = 5 * 60
          break
        except Exception:
          print('Failed to connect. Waiting for 5 seconds...')
          time.sleep(5)      

    return self.__instance
  
  def getStatus(self, id):
    raw_status = self.connection.get(id)
    
    if raw_status == None:
      return None

    status = raw_status.decode("utf-8")
    return status

  def saveStatus(self, id, status):
    self.connection.set(id, status, ex=self.expire_time)
