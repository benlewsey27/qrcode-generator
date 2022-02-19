from helpers.kafka import KafkaHelper
import logging
import os
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
  for message in KafkaHelper.instance().getConsumer():
    logger.debug("PROCESSING MESSAGE: %s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))

    # TODO: Generate QR code here!
    
    KafkaHelper.instance().getConsumer().commit()


if __name__ == '__main__':
  if 'DEBUG' in os.environ and os.environ.get('DEBUG') == '1':
    logger.setLevel(logging.DEBUG)

  if 'KAFKA_HOST' not in os.environ:
    logger.error('KAFKA_HOST is not defined.')
    sys.exit(1)

  if 'KAFKA_TOPIC' not in os.environ:
    logger.error('KAFKA_TOPIC is not defined.')
    sys.exit(1)

  if 'KAFKA_CONSUMER_GROUP' not in os.environ:
    logger.error('KAFKA_PARTITIONS is not defined.')
    sys.exit(1)

  KafkaHelper.instance({
    'kafka_host': os.environ.get('KAFKA_HOST'),
    'kafka_topic': os.environ.get('KAFKA_TOPIC'),
    'kafka_consumer_group': os.environ.get('KAFKA_CONSUMER_GROUP')
  })

  main()
