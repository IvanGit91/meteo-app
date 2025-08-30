# Meteorological Forecasting App

A Flask-based application that generates weather forecasts for sensors located at meteorological stations across different cities. The app uses Celery for background task processing and PostgreSQL for data storage.

## Features

- Weather forecast generation for city-based sensor stations
- Background task processing with Celery and Redis
- PostgreSQL database for data persistence
- Docker containerization for easy deployment
- Task monitoring with Flower dashboard

## Requirements

- Python 3.10+
- Docker and Docker Compose
- PostgreSQL

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd meteorological-app
```

2. Copy the DB environment and adapt to your configuration:
```bash
cp .env-db-local.example .env-db-local
```

3. Build and start the services:
```bash
docker-compose up --build
```

This will start:
- Flask API on `http://localhost:5000`
- PostgreSQL database on port `5433`
- Redis for task queue
- Celery worker for background processing
- Flower dashboard on `http://localhost:5555`

### Local Development

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up DB environment variables:
```bash
cp .env-db-local .env
```

4. Start PostgreSQL and Redis services (or use Docker for just the databases):
```bash
docker-compose up db redis
```

## Database Setup

### Initialize and migrate the database, using tha make command:

```bash
# Initialize migration repository (first time only)
make db-init

# Create migration
make db-migrate -m "Initial migration"

# Apply migrations
make db-upgrade
```

### To reset the database, using tha make command
```bash
# Initialize migration repository (first time only)
make db-init

# Drop all the table

# Recreate the alembic_version table, pretending to be fixed
make db-stamp-head

# Truncate the alembic_version table

# Apply migrations
make db-upgrade
```

## Usage

### Start the application:

**With Docker:**
```bash
docker-compose up
```

**Local development:**
```bash
python app.py
```

### Access the services:

- API: `http://localhost:5000`
- Flower Dashboard: `http://localhost:5555`

## Project Structure

```
meteorological-app/
├── app/
│   ├── server/          # Flask application core
│   └── tests/           # Test suite
├── migrations/          # Database migrations
├── app.py              # Application entry point
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # Docker services configuration
└── Dockerfile         # Container build instructions
```

## Testing

Run the test suite:
```bash
pytest app/tests/
```

## Future Development

The following features and improvements are planned for upcoming releases:

### 🚀 Planned Features

- **Kafka Integration**: Implement Apache Kafka for real-time sensor data streaming
  - Message broker for sensor forecasting data
  - Integration with Celery workers for async processing
  - Enhanced scalability for high-volume sensor networks

- **Enhanced Forecasting Models**: 
  - Machine learning integration for improved prediction accuracy
  - Historical data analysis and trend prediction
  - Multi-model ensemble forecasting

- **API Improvements**:
  - RESTful API endpoints for sensor management
  - Real-time WebSocket connections for live updates
  - API rate limiting and authentication

- **Monitoring & Observability**:
  - Application performance monitoring (APM)
  - Enhanced logging and metrics collection
  - Health check endpoints

### 🐛 Bug Fixes & Technical Improvements

- Code refactoring for better maintainability
- Performance optimizations for database queries
- Enhanced error handling and validation
- Security improvements and vulnerability patches
- Docker image optimization for smaller footprint

### 📊 Data Management

- Data retention policies for sensor readings
- Automated backup and recovery procedures
- Data export/import functionality
- Advanced querying capabilities

### 🔧 Infrastructure

- Kubernetes deployment configurations
- CI/CD pipeline implementation
- Multi-environment support (dev, staging, production)
- Load balancing and horizontal scaling

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
