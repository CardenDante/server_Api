# app/middleware/auth.py
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_api_key
import time
from app.utils.logger import logger

security = HTTPBearer()

class AuthMiddleware:
    async def __call__(self, request: Request, call_next):
        start_time = time.time()
        
        # Skip auth for login route
        if request.url.path == f"{request.app.prefix}/auth/token":
            response = await call_next(request)
            return response
            
        try:
            credentials: HTTPAuthorizationCredentials = await security(request)
            # Verify token or API key here
            if not credentials:
                raise HTTPException(status_code=403, detail="Invalid authentication")
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Auth error: {str(e)}")
            raise HTTPException(status_code=403, detail="Invalid authentication")

        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        return response