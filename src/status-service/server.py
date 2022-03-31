from flask import Flask, request
from helpers import filters
from helpers.redis import RedisHelper
import logging
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


@app.route('/status', methods=['POST'])
def getStatus():
  if 'id' not in request.json or type(request.json['id']) != str:
    return { 'status': 400, 'message': 'id either not found in body or invalid.' }, 400
 
  id = request.json['id']

  status = RedisHelper.instance().getStatus(id)
  if status == None:
    return { 'status': 404, 'message': 'QR code not found' }, 404

  return { 'id': id, 'status': status }, 200


@app.route('/update', methods=['POST'])
def update():
  if 'id' not in request.json or type(request.json['id']) != str:
    return { 'message': 'id either not found in body or invalid.' }, 400
  
  valid_states = ['requested', 'processing', 'done']
  if 'status' not in request.json or type(request.json['status']) != str or request.json['status'] not in valid_states:
    return { 'message': 'status either not found in body or invalid.' }, 400

  id = request.json['id']
  status = request.json['status']

  RedisHelper.instance().saveStatus(id, status)

  return { 'id': id, 'status': status }, 200


if __name__ == '__main__':
  if 'DEBUG' in os.environ and os.environ.get('DEBUG') == '1':
    logger.setLevel(logging.DEBUG)
  
  if 'REDIS_HOST' not in os.environ:
    logger.error('REDIS_HOST is not defined.')
    sys.exit(1)

  if 'REDIS_PORT' not in os.environ:
    logger.error('REDIS_PORT is not defined.')
    sys.exit(1)

  redis_host = os.environ.get('REDIS_HOST')
  redis_port = os.environ.get('REDIS_PORT')

  RedisHelper.instance(redis_host, redis_port)

  app.run(host='0.0.0.0', port=8000)
