import psutil
import platform
import subprocess
import os
from datetime import datetime
from typing import Dict, Any

def get_system_stats() -> Dict[str, Any]:
   return {
       "timestamp": datetime.now().isoformat(),
       "cpu": {
           "percent": psutil.cpu_percent(interval=1),
           "cores": psutil.cpu_count(),
           "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
       },
       "memory": {
           "total": psutil.virtual_memory().total,
           "available": psutil.virtual_memory().available,
           "percent": psutil.virtual_memory().percent
       },
       "disk": {
           "total": psutil.disk_usage('/').total,
           "used": psutil.disk_usage('/').used, 
           "free": psutil.disk_usage('/').free,
           "percent": psutil.disk_usage('/').percent
       },
       "network": psutil.net_io_counters()._asdict(),
       "system": {
           "platform": platform.system(),
           "release": platform.release(),
           "version": platform.version()
       },
       "services": get_service_status()
   }

def get_process_stats() -> Dict[str, Any]:
   processes = []
   for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
       try:
           processes.append(proc.info)
       except (psutil.NoSuchProcess, psutil.AccessDenied):
           continue
   return {
       "total_processes": len(processes),
       "processes": sorted(processes, key=lambda x: x.get('cpu_percent', 0), reverse=True)[:10]
   }

def get_service_status() -> Dict[str, bool]:
   services = ['nginx', 'docker']
   status = {}
   for service in services:
       try:
           result = subprocess.run(['systemctl', 'is-active', service], 
                                 capture_output=True, text=True)
           status[service] = result.returncode == 0
       except Exception:
           status[service] = False
   return status