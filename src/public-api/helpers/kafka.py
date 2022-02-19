from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
import json
import time

class KafkaHelper():
  __instance = None

  def __init__(self):
    raise RuntimeError('Call instance() instead')

  @classmethod
  def instance(self, kafka_host=None):
    if self.__instance is None:
      self.__instance = self.__new__(self)
      while True:
        try:
          self.producer = KafkaProducer(bootstrap_servers=kafka_host, value_serializer=lambda m: json.dumps(m).encode())
          self.adminClient = KafkaAdminClient(bootstrap_servers=kafka_host)
          break
        except Exception:
          print('Failed to connect. Waiting for 5 seconds...')
          time.sleep(5)      

    return self.__instance

  def createTopic(self, topic_name, num_partitions):
    self.adminClient.create_topics([NewTopic(topic_name, num_partitions=int(num_partitions), replication_factor=1)])

  def send(self, kafka_topic, message):
    self.producer.send(kafka_topic, message)
