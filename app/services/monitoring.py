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
            "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
            "load_average": os.getloadavg()
        },
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "percent": psutil.virtual_memory().percent,
            "swap": psutil.swap_memory()._asdict()
        },
        "disk": {
            mount.mountpoint: psutil.disk_usage(mount.mountpoint)._asdict()
            for mount in psutil.disk_partitions(all=True)
        },
        "network": {
            "io": psutil.net_io_counters()._asdict(),
            "connections": len(psutil.net_connections()),
            "interfaces": psutil.net_if_stats()
        },
        "system": {
            "platform": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "uptime": datetime.now().timestamp() - psutil.boot_time()
        }
    }

def get_process_stats() -> Dict[str, Any]:
    processes = []
    watched_services = ['nginx', 'docker', 'apache2', 'mysql', 'postgresql']
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            if proc.info['name'] in watched_services:
                proc_info = proc.info
                proc_info['ports'] = get_process_ports(proc.info['pid'])
                processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    return {
        "total_processes": len(processes),
        "services": {
            service: [p for p in processes if p['name'] == service]
            for service in watched_services
        },
        "top_cpu": sorted(processes, key=lambda x: x.get('cpu_percent', 0), reverse=True)[:10]
    }

def get_process_ports(pid: int) -> list:
    try:
        connections = psutil.Process(pid).connections()
        return [conn.laddr.port for conn in connections if conn.status == 'LISTEN']
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return []