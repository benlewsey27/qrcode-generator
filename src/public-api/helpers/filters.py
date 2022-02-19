import logging

class HealthFilter(logging.Filter):
  def filter(self, record):
    return '/health' not in record.getMessage()
