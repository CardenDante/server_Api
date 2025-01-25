# app/api/routes/logs.py
from fastapi import APIRouter, HTTPException
from app.core.config import settings
import os
from typing import List, Optional
from datetime import datetime, timedelta

router = APIRouter(prefix="/logs", tags=["logs"])

@router.get("/")
async def get_logs(
    lines: Optional[int] = 100,
    level: Optional[str] = None,
    since: Optional[str] = None
) -> dict:
    try:
        if not os.path.exists(settings.LOG_FILE):
            return {"logs": [], "message": "No logs found"}

        with open(settings.LOG_FILE, 'r') as f:
            logs = f.readlines()

        if since:
            since_date = datetime.fromisoformat(since)
            logs = [
                log for log in logs
                if datetime.strptime(log.split()[0], '%Y-%m-%d') >= since_date
            ]

        if level:
            logs = [log for log in logs if level.upper() in log]

        return {
            "total_lines": len(logs),
            "logs": logs[-lines:]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading logs: {str(e)}"
        )

@router.delete("/")
async def clear_logs() -> dict:
    try:
        if os.path.exists(settings.LOG_FILE):
            with open(settings.LOG_FILE, 'w') as f:
                f.write('')
        return {"message": "Logs cleared successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing logs: {str(e)}"
        )