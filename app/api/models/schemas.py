# app/api/models/schemas.py
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

class SystemStats(BaseModel):
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_stats: Dict
    timestamp: datetime

class ProcessInfo(BaseModel):
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float

class ProcessStats(BaseModel):
    total_processes: int
    processes: List[ProcessInfo]

class NginxStatus(BaseModel):
    running: bool
    error: Optional[str] = None

class NginxAction(BaseModel):
    status: str
    message: str

class LogEntry(BaseModel):
    timestamp: datetime
    level: str
    message: str

class LogResponse(BaseModel):
    total_lines: int
    logs: List[str]

class ErrorResponse(BaseModel):
    detail: str

class SuccessResponse(BaseModel):
    message: str