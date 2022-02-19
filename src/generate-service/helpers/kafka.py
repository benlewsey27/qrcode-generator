from kafka import KafkaConsumer, KafkaAdminClient
import json
import time

class KafkaHelper():
  __instance = None

  def __init__(self):
    raise RuntimeError('Call instance() instead')

  @classmethod
  def instance(self, params=None):
    if self.__instance is None:
      self.__instance = self.__new__(self)

      kafka_host = params['kafka_host']
      kafka_topic = params['kafka_topic']
      kafka_consumer_group = params['kafka_consumer_group']

      while True:
        try:
          self.adminClient = KafkaAdminClient(bootstrap_servers=kafka_host)
          break
        except Exception:
          print('Failed to connect. Waiting for 5 seconds...')
          time.sleep(5)
      
      while True:
        if kafka_topic in self.adminClient.list_topics():
          break
        else:
          print('Topic not found. Waiting for 5 seconds...')
          time.sleep(5)

      self.consumer = KafkaConsumer(
        kafka_topic,
        group_id=kafka_consumer_group,
        bootstrap_servers=kafka_host,
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        value_deserializer=lambda m: json.loads(m.decode('ascii'))
      )

    return self.__instance

  def getConsumer(self):
    return self.consumer
