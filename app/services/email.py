# app/services/email.py
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from app.core.config import settings
import logging
from datetime import datetime

async def send_error_email(error_message: str) -> bool:
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_FROM
        msg['To'] = settings.EMAIL_FROM
        msg['Subject'] = f"Server Error Alert - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        body = f"""
        Error Details:
        --------------
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Error: {error_message}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_FROM, settings.EMAIL_PASSWORD)
            server.send_message(msg)
            
        logging.info(f"Error email sent successfully")
        return True
            
    except Exception as e:
        logging.error(f"Failed to send error email: {str(e)}")
        return False

async def send_status_report(stats: dict) -> bool:
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_FROM
        msg['To'] = settings.ALERT_EMAIL
        msg['Subject'] = f"Server Status Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        body = f"""
        Server Status Report
        -------------------
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        CPU Usage: {stats['cpu']['percent']}%
        Memory Usage: {stats['memory']['percent']}%
        Disk Usage: {stats['disk']['percent']}%
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_FROM, settings.EMAIL_PASSWORD)
            server.send_message(msg)
            
        logging.info("Status report email sent successfully")
        return True
            
    except Exception as e:
        logging.error(f"Failed to send status report: {str(e)}")
        return False