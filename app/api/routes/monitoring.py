# app/api/routes/monitoring.py
from fastapi import APIRouter
from app.services.monitoring import get_system_stats, get_process_stats, get_process_ports
from app.services.email import send_status_report
from typing import Dict, Any

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

@router.get("/stats", response_model=Dict[str, Any])
async def get_stats():
   stats = get_system_stats()
   await send_status_report(stats)
   return stats

@router.get("/processes")
async def get_processes():
   return get_process_stats()

@router.get("/process/{pid}/ports")
async def get_ports(pid: int):
   return {"ports": get_process_ports(pid)}