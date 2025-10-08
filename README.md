#   First variant of Skyluxe and a Failed project of mine, the successful one is there in another repository

A SOLID-compliant climate analysis platform built with FastAPI and React, following clean architecture principles.

## 🏗️ Architecture Overview

This project implements a decoupled, testable, and extensible system based on SOLID principles:

- **Single Responsibility Principle (SRP)**: Each class has one reason to change
- **Open/Closed Principle (OCP)**: Open for extension, closed for modification
- **Liskov Substitution Principle (LSP)**: Derived classes must be substitutable for base classes
- **Interface Segregation Principle (ISP)**: Clients shouldn't depend on interfaces they don't use
- **Dependency Inversion Principle (DIP)**: Depend on abstractions, not concretions

## 📁 Project Structure

```
skyluxe/
├── api/                    # FastAPI routers (HTTP layer)
├── services/               # Business logic services
├── clients/               # External API clients
├── calculators/           # Metric calculation implementations
├── interfaces/            # Abstract base classes
├── core/                  # Dependency injection & configuration
└── main.py              # Application entry point
```

## 🚀 Quick Start

### Backend Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the development server:**
   ```bash
   python -m skyluxe.main
   ```

3. **Access the API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### API Endpoints

- `POST /analysis/` - Perform climate analysis
- `GET /analysis/metrics` - Get available metrics
- `GET /analysis/health` - Health check

### Example Usage

```bash
# Perform climate analysis
curl -X POST "http://localhost:8000/analysis/" \
  -H "Content-Type: application/json" \
  -d '{
    "location": {
      "latitude": 40.7128,
      "longitude": -74.0060
    },
    "date_range": {
      "start_date": "2023-01-01",
      "end_date": "2023-01-31"
    }
  }'
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=skyluxe
```

## 🔧 Development

### Code Quality

```bash
# Format code
black skyluxe/

# Lint code
flake8 skyluxe/

# Type checking
mypy skyluxe/
```

## 📊 Available Metrics

- **Temperature Analysis**: Mean, max, min temperatures with category breakdowns
- **Precipitation Analysis**: Total precipitation, dry/wet periods, intensity categories

## 🌟 Key Features

- **Dependency Injection**: Clean separation of concerns
- **Interface-based Design**: Easy to extend with new data sources and calculators
- **Error Handling**: Comprehensive error handling and logging
- **Data Validation**: Pydantic models for request/response validation
- **SOLID Compliance**: Maintainable and extensible architecture

## 🔮 Future Enhancements

- Additional weather metrics (wind, humidity, comfort index)
- Data export capabilities (CSV, JSON, PDF)
- User authentication and personalization
- Advanced visualization dashboard
- Caching and performance optimization

## 📝 License

MIT License - see LICENSE file for details.
