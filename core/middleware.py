# myproject/middleware.py
import time
import logging

logger = logging.getLogger(__name__)

class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        print(f"Request to {request.path} took {duration:.3f} seconds.")
        logger.info(f"Request to {request.path} took {duration:.3f} seconds.")
        return response
