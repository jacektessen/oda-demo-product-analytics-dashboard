# ODA API Stats Service

A microservice-based application that fetches, processes, and caches product statistics from the ODA API.

## Project Structure

```
.
├── api-service/          # FastAPI backend service
├── client/              # Next.js frontend application
├── redis/               # Redis configuration
├── tests/               # API tests
└── docker/             # Docker configurations
```

## Features

- Fetches and aggregates product data from ODA API
- Caches processed data in Redis
- Provides RESTful API endpoints for statistics
- Automatic data refresh every 30 minutes
- Real-time health monitoring
- Comprehensive API testing suite

## Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

## Getting Started

1. Clone the repository

```bash
git clone https://github.com/jacektessen/oda-demo-product-analytics-dashboard.git
```

2. Start the services

```bash
docker-compose up -d
```

The following services will be available:
- API Service: http://localhost:8000
- Frontend: http://localhost:3000
- Redis: localhost:6379

## API Endpoints

### Statistics
```
GET /api/stats
```
Returns aggregated product statistics including:
- Total product count
- Average price
- Price ranges distribution
- Top 10 brands
- Category distribution
- Cache information

### Health Check
```
GET /health
```
Returns health status of the service and its dependencies.

## Running Tests

Tests are maintained separately from the main services. To run the tests:

1. Ensure services are running
```bash
docker-compose up -d
```

2. Run tests locally
```bash
cd tests
npm install
npm test
```

View test reports:
```bash
npm run report
```

## Configuration

Environment variables:
- `API_SERVICE_URL`: API service URL (default: http://localhost:8000)
- `REDIS_HOST`: Redis host (default: redis)
- `REDIS_PORT`: Redis port (default: 6379)

## Cache Strategy

- Initial cache population on service startup
- Automatic refresh every 30 minutes
- Cache TTL: 1 hour
- Fallback mechanism if cache is unavailable

## Development

### API Service Development
```bash
cd api-service
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development
```bash
cd client
npm install
npm run dev
```

### Running Tests During Development
```bash
cd tests
npm install
npm run test:ui  # For UI mode
npm run test:debug  # For debug mode
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and ensure they pass
4. Submit a pull request