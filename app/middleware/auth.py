# app/middleware/auth.py
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
import time
from app.utils.logger import logger

security = HTTPBearer()

class AuthMiddleware:
    async def __call__(self, request: Request, call_next):
        public_paths = [
            f"{settings.API_V1_STR}/auth/token",
            "/",
            "/docs",
            "/openapi.json",
            f"{settings.API_V1_STR}/openapi.json",
            "/redoc",
            "/favicon.ico",
            "/docs/oauth2-redirect"
        ]
        
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)
            
        try:
            credentials = await security(request)
            if not credentials:
                raise HTTPException(status_code=403)
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Auth error: {str(e)}")
            raise HTTPException(status_code=403, detail="Invalid authentication")

        response = await call_next(request)
        response.headers["X-Process-Time"] = str(time.time() - start_time)
        return response