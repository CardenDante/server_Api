# app/api/routes/nginx.py
from fastapi import APIRouter, HTTPException
from app.services.nginx import NginxService
from app.services.email import send_error_email
from typing import Dict

router = APIRouter(prefix="/nginx", tags=["nginx"])

@router.get("/status")
async def get_nginx_status() -> Dict:
    return await NginxService.get_status()

@router.post("/{action}")
async def manage_nginx(action: str) -> Dict:
    try:
        result = await NginxService.manage_service(action)
        if result["status"] == "error":
            await send_error_email(result["message"])
            raise HTTPException(status_code=500, detail=result["message"])
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/config")
async def get_nginx_config():
    config = await NginxService.get_config()
    if config is None:
        raise HTTPException(status_code=500, detail="Failed to get Nginx configuration")
    return {"config": config}

@router.post("/test-config")
async def test_nginx_config():
    result = await NginxService.test_config()
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result