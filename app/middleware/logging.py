# app/middleware/logging.py
from fastapi import Request
import time
from app.utils.logger import logger

class LoggingMiddleware:
    async def __call__(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log response
            logger.info(
                f"Response: {request.method} {request.url.path} "
                f"- Status: {response.status_code} "
                f"- Time: {process_time:.3f}s"
            )
            return response
            
        except Exception as e:
            logger.error(
                f"Error: {request.method} {request.url.path} "
                f"- Error: {str(e)}"
            )
            raise