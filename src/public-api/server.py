from flask import Flask, send_file, request as request_data
from helpers import filters
from helpers.kafka import KafkaHelper
import requests
import logging
import random
import string
import os
import sys

logging.basicConfig(level=logging.INFO)

werkzeug = logging.getLogger('werkzeug')
werkzeug.addFilter(filters.HealthFilter())

logger = logging.getLogger(__name__)

app = Flask(__name__)


def generate_id():
  return ''.join(random.choices(string.ascii_letters + string.digits, k=16)).lower()


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
  if 'data' not in request_data.json or type(request_data.json['data']) != str:
    return { 'status': 400, 'message': 'data either not found in body or invalid.' }, 400

  data = request_data.json['data']
  request_id = generate_id()

  logger.debug(f'Generating QR code {request_id} with data {data}...')

  payload = { 'id': request_id, 'data': data }
  KafkaHelper.instance().send(kafka_topic, payload)

  requests.post(f'{status_service_host}/update', json={ 'id': request_id, 'status': 'requested' })
  return { 'status': 200, 'id': request_id, 'message': 'QR code requested successfully.' }, 200


@app.route('/fetch/<id>', methods=['GET'])
def fetch_qrcode(id):
  logger.debug(f'Fetching QR code with id {id}...')

  response = requests.post(f'{status_service_host}/status', json={ 'id': id })
  response_data = response.json()

  if response.status_code == 404:
    return { 'status': 404, 'message': 'QR code not found' }, 404

  if response_data['status'] != 'done':
    return { 'status': 400, 'message': 'QR code is still processing. Please try again later.' }, 400

  if not os.path.exists(f'/tmp/{id}.png'):
    logger.error(f'QR code with id {id} has finished, but file is not found!')
    return { 'status': 500, 'message': 'Internal Server Error' }, 500

  return send_file(f'/tmp/{id}.png', as_attachment=True)


@app.route('/status/<id>', methods=['GET'])
def get_status(id):
  logger.debug(f'Getting status for QR code with id {id}...')

  response = requests.post(f'{status_service_host}/status', json={ 'id': id })

  if response.status_code == 404:
    return { 'status': 404, 'message': 'QR code not found' }, 404

  data = response.json()
  status = data['status']

  return { 'id': id, 'status': status }, 200


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

  if 'STATUS_SERVICE_HOST' not in os.environ:
    logger.error('STATUS_SERVICE_HOST is not defined.')
    sys.exit(1)

  kafka_host = os.environ.get('KAFKA_HOST')
  kafka_topic = os.environ.get('KAFKA_TOPIC')
  kafka_partitions = os.environ.get('KAFKA_PARTITIONS')
  status_service_host = os.environ.get('STATUS_SERVICE_HOST')

  KafkaHelper.instance(kafka_host).createTopic(kafka_topic, kafka_partitions)

  app.run(host='0.0.0.0', port=8000)
