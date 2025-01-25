# Server Management API

## Description
The Server Management API is a FastAPI application that provides endpoints for managing server logs, monitoring system status, and handling authentication.

## Features
- Retrieve and clear server logs.
- Monitor system performance and status.
- Authentication and authorization for secure access.
- Rate limiting to prevent abuse.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd server_Api
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
- Start the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
- Access the API documentation at: [http://localhost:8000/api/v1/openapi.json](http://localhost:8000/api/v1/openapi.json)

### API Endpoints
- **GET /api/v1/logs/**: Retrieve logs.
  - Query parameters:
    - `lines`: Number of log lines to return (default is 100).
    - `level`: Filter logs by severity level.
    - `since`: Filter logs since a specific date.
  
- **DELETE /api/v1/logs/**: Clear logs.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
