# Quick Start Guide

## Setup (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database with sample data
python -m app.init_db

# 3. Run the server
python run.py
```

## Access

- **Swagger UI**: http://localhost:8000/docs
- **API Base**: http://localhost:8000/api

## Quick Tests

### Books
```bash
# Get all books
curl http://localhost:8000/api/books

# Search books
curl "http://localhost:8000/api/search/books?q=tolkien"

# Create a book
curl -X POST http://localhost:8000/api/books \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Book","author":"Test Author","isbn":"978-1234567890","total_copies":1,"available_copies":1}'
```

### Members
```bash
# Get all members
curl http://localhost:8000/api/members

# Create a member
curl -X POST http://localhost:8000/api/members \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","phone":"555-0000"}'
```

### Borrowings
```bash
# Borrow a book
curl -X POST http://localhost:8000/api/borrowings \
  -H "Content-Type: application/json" \
  -d '{"book_id":1,"member_id":1,"due_date":"2026-02-28"}'

# Get overdue books
curl http://localhost:8000/api/borrowings/overdue
```

### Statistics (NEW!)
```bash
# Get library statistics
curl http://localhost:8000/api/stats/overview

# Get popular books
curl http://localhost:8000/api/stats/popular-books
```

## Key Features

✅ **CRUD Operations** - Full create, read, update, delete for books, members, borrowings
✅ **Advanced Search** - Search books by title, author, ISBN, or genre
✅ **Statistics Dashboard** - Real-time library metrics and popular books
✅ **Validation** - Automatic input validation with detailed error messages
✅ **Documentation** - Auto-generated interactive API docs
✅ **Business Logic** - Fine calculation, overdue tracking, availability checks

## API Endpoints Summary

| Feature | Endpoint | Method |
|---------|----------|--------|
| List books | `/api/books` | GET |
| Create book | `/api/books` | POST |
| Search books | `/api/search/books?q=query` | GET |
| List members | `/api/members` | GET |
| Borrow book | `/api/borrowings` | POST |
| Return book | `/api/borrowings/{id}/return` | PUT |
| Get stats | `/api/stats/overview` | GET |
| Popular books | `/api/stats/popular-books` | GET |

See full documentation in `README.md` and `EXTRA_FEATURES.md`

