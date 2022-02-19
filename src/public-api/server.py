from flask import Flask, request
from helpers import filters
from helpers.kafka import KafkaHelper
import logging
import uuid
import os
import sys

logging.basicConfig(level=logging.INFO)

werkzeug = logging.getLogger('werkzeug')
werkzeug.addFilter(filters.HealthFilter())

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/health')
def health():
  return '', 200


@app.errorhandler(404)
def catch(err):
  return 'Error: Route Not Found', 404


@app.errorhandler(405)
def catch(err):
  return 'Error: Invalid Method', 405


@app.route('/generate', methods=['POST'])
def generate_qrcode():
  if 'data' not in request.json or type(request.json['data']) != str:
    return { 'status': 400, 'message': 'data either not found in body or invalid.' }, 400

  data = request.json['data']
  request_id = uuid.uuid4()

  logger.debug(f'Generating QR code {request_id} with data {data}...')

  payload = { 'id': str(request_id), 'data': data }
  KafkaHelper.instance().send(kafka_topic, payload)

  return { 'status': 200, 'id': str(request_id), 'message': 'QR code requested successfully.' }, 200


@app.route('/fetch/<id>', methods=['GET'])
def fetch_qrcode(id):
  logger.debug(f'Fetching QR code with id {id}...')

  return 'WARNING: fetch not implemented yet!', 200


@app.route('/status/<id>', methods=['GET'])
def get_status(id):
  logger.debug(f'Getting status for QR code with id {id}...')

  return 'WARNING: status not implemented yet!', 200


if __name__ == '__main__':
  if 'DEBUG' in os.environ and os.environ.get('DEBUG') == '1':
    logger.setLevel(logging.DEBUG)
  
  if 'KAFKA_HOST' not in os.environ:
    logger.error('KAFKA_HOST is not defined.')
    sys.exit(1)

  if 'KAFKA_TOPIC' not in os.environ:
    logger.error('KAFKA_TOPIC is not defined.')
    sys.exit(1)

  if 'KAFKA_PARTITIONS' not in os.environ:
    logger.error('KAFKA_PARTITIONS is not defined.')
    sys.exit(1)

  kafka_host = os.environ.get('KAFKA_HOST')
  kafka_topic = os.environ.get('KAFKA_TOPIC')
  kafka_partitions = os.environ.get('KAFKA_PARTITIONS')

  KafkaHelper.instance(kafka_host).createTopic(kafka_topic, kafka_partitions)

  app.run(host='0.0.0.0', port=8000)
