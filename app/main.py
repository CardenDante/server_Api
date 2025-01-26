# app/main.py
from fastapi import FastAPI, Depends
from app.core.security import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.middleware.auth import AuthMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.api.routes import server, nginx, logs, auth, monitoring  

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middlewares
app.middleware("http")(AuthMiddleware())
app.middleware("http")(LoggingMiddleware())
app.middleware("http")(RateLimitMiddleware(requests_per_minute=60))

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(server.router, prefix=settings.API_V1_STR)
app.include_router(nginx.router, prefix=settings.API_V1_STR)
app.include_router(logs.router, prefix=settings.API_V1_STR)
app.include_router(monitoring.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Server Management API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)