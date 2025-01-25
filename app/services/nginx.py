import subprocess
import logging
from typing import Dict, Optional
import psutil

class NginxService:
    @staticmethod
    async def get_status() -> Dict[str, bool]:
        try:
            for proc in psutil.process_iter(['name']):
                if 'nginx' in proc.info['name'].lower():
                    return {"running": True}
            return {"running": False}
        except Exception as e:
            logging.error(f"Error checking nginx status: {str(e)}")
            return {"running": False, "error": str(e)}

    @staticmethod
    async def manage_service(action: str) -> Dict[str, str]:
        valid_actions = ["start", "stop", "restart", "reload"]
        if action not in valid_actions:
            raise ValueError(f"Invalid action. Must be one of: {valid_actions}")

        try:
            result = subprocess.run(
                ["sudo", "systemctl", action, "nginx"],
                capture_output=True,
                text=True,
                check=True
            )
            return {"status": "success", "message": f"Nginx {action} successful"}
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to {action} Nginx: {e.stderr}"
            logging.error(error_msg)
            return {"status": "error", "message": error_msg}

    @staticmethod
    async def get_config() -> Optional[str]:
        try:
            result = subprocess.run(
                ["nginx", "-T"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to get Nginx config: {e.stderr}")
            return None

    @staticmethod
    async def test_config() -> Dict[str, str]:
        try:
            result = subprocess.run(
                ["nginx", "-t"],
                capture_output=True,
                text=True,
                check=True
            )
            return {"status": "success", "message": "Configuration test successful"}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": e.stderr}