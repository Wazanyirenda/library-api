# Library Management API

# API Features

- **Book Management**: Create, read, update, and delete books
- **Member Management**: Manage library members and their accounts
- **Borrowing System**: Track book borrowings, returns, and due dates
- **Advanced Search**: Unified search across books by title, author, ISBN, or genre
- **Statistics Dashboard**: Real-time library analytics and popular books tracking
- **Validation**: Comprehensive input validation with Pydantic
- **Error Handling**: Meaningful error messages and proper HTTP status codes
- **Filters**: Query parameters for filtering and searching
- **Overdue Tracking**: Automatic tracking and fine calculation for overdue books
- **Interactive Documentation**: Auto-generated Swagger UI and ReDoc
- **Type Safety**: Full type hints and validation

# Technologies

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database
- **Uvicorn**: ASGI server

## Installation


### Prerequisites

- Python 
- Python package installer

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd library-api
```

2. Create and activate a virtual environment:
```bash

python -m venv venv
venv\Scripts\activate

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database with sample data:
```bash
python -m app.init_db
```

This will create the SQLite database, set up tables, and insert sample data.

5. Start the server:
```bash

python run.py


uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

## Interactive API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Base URL
```
http://localhost:8000/api
```


