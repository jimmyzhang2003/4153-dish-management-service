import logging
from datetime import datetime
from flask import g, request

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Middleware logging before each request
def before_request_logging():
    g.start_time = datetime.now()
    logger.info(f"Incoming {request.method} request to {request.path} with data: {request.args.to_dict()}")

# Middleware logging after each request
def after_request_logging(response):
    duration = datetime.now() - g.start_time
    logger.info(f"Completed {request.method} request to {request.path} in {duration.total_seconds()} seconds with status code {response.status_code}")
    return response