# app/api/routes/server.py
from fastapi import APIRouter, HTTPException
from app.services.monitoring import get_system_stats
from app.services.email import send_error_email

router = APIRouter(prefix="/server", tags=["server"])

@router.get("/stats")
async def get_server_stats():
    try:
        stats = get_system_stats()
        return stats
    except Exception as e:
        error_msg = f"Error getting server stats: {str(e)}"
        await send_error_email(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)