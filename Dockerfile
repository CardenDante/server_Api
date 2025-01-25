# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# System dependencies with enhanced monitoring capabilities
RUN apt-get update && apt-get install -y \
   nginx \
   sudo \
   sysstat \
   iproute2 \
   net-tools \
   procps \
   && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p logs ssl

# Add user to sudoers for system commands
RUN echo "api ALL=(ALL) NOPASSWD: /usr/sbin/service nginx *" >> /etc/sudoers

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]