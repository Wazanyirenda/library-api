# Getting Started with Library Management API

This guide will help you set up and run the Library Management API on your local machine.

## Prerequisites

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package installer (comes with Python)
- **Git** (optional) - For cloning the repository

## Quick Start (5 minutes)

### Step 1: Set Up Virtual Environment

Open your terminal/command prompt and navigate to the project directory:

**Windows:**
```bash
cd library-api
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
cd library-api
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt, indicating the virtual environment is active.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI - Web framework
- Uvicorn - ASGI server
- SQLAlchemy - Database ORM
- Pydantic - Data validation
- And other necessary packages

### Step 3: Initialize Database

```bash
python -m app.init_db
```

This creates the SQLite database and populates it with sample data:
- 8 books
- 5 members
- 3 borrowing records

### Step 4: Start the Server

```bash
python run.py
```

You should see output like:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 5: Test the API

Open your web browser and go to:

**Interactive API Documentation (Swagger UI):**
```
http://localhost:8000/docs
```

**Alternative Documentation (ReDoc):**
```
http://localhost:8000/redoc
```

**Simple Health Check:**
```
http://localhost:8000/health
```

## Using the API

### Through Swagger UI (Easiest)

1. Open http://localhost:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the parameters/request body
5. Click "Execute"
6. View the response

### Through curl

**Get all books:**
```bash
curl http://localhost:8000/api/books
```

**Create a member:**
```bash
curl -X POST http://localhost:8000/api/members \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Your Name",
    "email": "your.email@example.com",
    "phone": "555-1234"
  }'
```

**Borrow a book:**
```bash
curl -X POST http://localhost:8000/api/borrowings \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "member_id": 1,
    "due_date": "2026-02-28"
  }'
```

### Through Python

```python
import requests

# Get all books
response = requests.get("http://localhost:8000/api/books")
books = response.json()
print(f"Found {len(books)} books")

# Get available books only
response = requests.get("http://localhost:8000/api/books?available=true")
available_books = response.json()
print(f"Available: {len(available_books)} books")
```

## Sample Data

After running `python -m app.init_db`, your database will have:

### Books
1. The Great Gatsby by F. Scott Fitzgerald
2. To Kill a Mockingbird by Harper Lee
3. 1984 by George Orwell
4. Pride and Prejudice by Jane Austen
5. The Catcher in the Rye by J.D. Salinger
6. The Hobbit by J.R.R. Tolkien (1 copy borrowed)
7. Harry Potter and the Philosopher's Stone by J.K. Rowling (1 copy borrowed)
8. The Lord of the Rings by J.R.R. Tolkien (1 copy overdue)

### Members
1. John Doe (has 1 borrowed book)
2. Jane Smith (has 1 borrowed book)
3. Bob Johnson (has 1 overdue book)
4. Alice Williams
5. Charlie Brown (inactive)

## API Endpoints Overview

### Books (`/api/books`)
- `GET /api/books` - List all books (with optional filters)
- `GET /api/books/{id}` - Get specific book
- `GET /api/books/{id}/availability` - Check availability
- `POST /api/books` - Create new book
- `PUT /api/books/{id}` - Update book
- `DELETE /api/books/{id}` - Delete book

### Members (`/api/members`)
- `GET /api/members` - List all members (with optional filters)
- `GET /api/members/{id}` - Get specific member
- `GET /api/members/{id}/history` - Get borrowing history
- `GET /api/members/{id}/borrowings` - Get active borrowings
- `POST /api/members` - Create new member
- `PUT /api/members/{id}` - Update member
- `DELETE /api/members/{id}` - Delete member

### Borrowings (`/api/borrowings`)
- `GET /api/borrowings` - List all borrowings (with optional filters)
- `GET /api/borrowings/overdue` - Get overdue borrowings
- `GET /api/borrowings/{id}` - Get specific borrowing
- `POST /api/borrowings` - Borrow a book
- `PUT /api/borrowings/{id}/return` - Return a book
- `PUT /api/borrowings/{id}/renew` - Renew a borrowing

## Common Tasks

### Reset the Database

```bash
# Delete the database file
rm library.db  # Linux/macOS
del library.db  # Windows

# Reinitialize
python -m app.init_db
```

### Stop the Server

Press `CTRL+C` in the terminal where the server is running.

### Deactivate Virtual Environment

```bash
deactivate
```

### View Database Contents

You can use any SQLite browser, or:

```bash
# Install sqlite3 command-line tool if not already installed
sqlite3 library.db

# Inside sqlite3:
.tables                        # List all tables
SELECT * FROM books;           # View all books
SELECT * FROM members;         # View all members
SELECT * FROM borrowing_records;  # View all borrowings
.quit                          # Exit
```

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, you can run on a different port:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Module Not Found Error

Make sure your virtual environment is activated:
- You should see `(venv)` in your terminal prompt
- Run `pip list` to verify packages are installed

### Database Locked Error

If you get a database locked error:
1. Stop all running instances of the server
2. Close any database browsers
3. Restart the server

### Import Errors

If you get import errors, reinstall dependencies:

```bash
pip install --upgrade -r requirements.txt
```

## Next Steps

1. **Explore the API**: Use the Swagger UI at http://localhost:8000/docs
2. **Read the Documentation**: Check out `README.md` for detailed API information
3. **Try Examples**: See `API_EXAMPLES_FASTAPI.md` for comprehensive examples
4. **Customize**: Modify the code to fit your needs

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review [API_EXAMPLES_FASTAPI.md](API_EXAMPLES_FASTAPI.md) for usage examples
- Open an issue on GitHub if you encounter problems

## Development Mode Features

When running in development mode (with `--reload`), the server will:
- Automatically restart when you make code changes
- Show detailed error messages
- Enable hot reloading

## Production Deployment

For production deployment, see the FastAPI documentation:
https://fastapi.tiangolo.com/deployment/

Basic production command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

For better performance with multiple workers:
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

Enjoy building with the Library Management API! 📚

