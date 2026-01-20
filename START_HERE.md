# 📚 Library Management API - START HERE

Welcome! This is a complete FastAPI-based library management system.

## 🚀 Quick Start (3 Steps)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Initialize
python -m app.init_db

# 3. Run
python run.py
```

Then open: **http://localhost:8000/docs**

## ✨ What You Get

### Core Features
✅ **Books Management** - Full CRUD with availability tracking
✅ **Members Management** - Registration, profiles, history
✅ **Borrowing System** - Checkout, return, renewals, fines

### Extra Features (Bonus!)
⭐ **Advanced Search** - One endpoint to search all book fields
⭐ **Statistics Dashboard** - Real-time metrics & popular books

## 📖 Documentation

| File | Purpose |
|------|---------|
| **QUICK_START.md** | API examples & quick tests |
| **README.md** | Complete API documentation |
| **EXTRA_FEATURES.md** | Search & statistics details |
| **GETTING_STARTED.md** | Setup & troubleshooting |
| **PROJECT_SUMMARY.md** | Architecture & design decisions |

## 🎯 Try It Out

### Using Swagger UI (Easiest)
1. Go to http://localhost:8000/docs
2. Click any endpoint
3. Click "Try it out"
4. Execute!

### Using curl
```bash
# Get all books
curl http://localhost:8000/api/books

# Search for books
curl "http://localhost:8000/api/search/books?q=tolkien"

# Get library statistics
curl http://localhost:8000/api/stats/overview

# Get popular books
curl http://localhost:8000/api/stats/popular-books
```

## 📊 API Overview

**19 Endpoints** across 5 categories:

1. **Books** (7 endpoints) - CRUD + availability
2. **Members** (7 endpoints) - CRUD + history
3. **Borrowings** (6 endpoints) - Checkout + return + renew
4. **Search** (1 endpoint) - Unified book search ⭐
5. **Statistics** (2 endpoints) - Metrics + analytics ⭐

## 🏗️ Architecture

```
Minimal & Clean Design:
├── 📁 app/
│   ├── 📁 routers/     - API endpoints (5 files)
│   ├── 📄 models.py    - Database models
│   ├── 📄 schemas.py   - Request/response validation
│   ├── 📄 main.py      - FastAPI app
│   └── 📄 init_db.py   - Sample data
├── 📄 requirements.txt - 6 dependencies
└── 📄 run.py          - Server entry
```

**Total Code**: ~1,100 lines (very minimal!)

## 🎁 Extra Features (Why They Matter)

### 1. Search 🔍
**Problem**: Users don't know if "Tolkien" is in title or author
**Solution**: One search endpoint checks all fields
```bash
curl "http://localhost:8000/api/search/books?q=tolkien"
```

### 2. Statistics 📊
**Problem**: No visibility into library performance
**Solution**: Real-time dashboard metrics
```bash
curl http://localhost:8000/api/stats/overview
# Returns: books, members, borrowings, fines, etc.

curl http://localhost:8000/api/stats/popular-books
# Returns: Most borrowed books
```

## 🔥 Key Features

- ✅ **Auto-generated Docs** - Swagger UI & ReDoc
- ✅ **Input Validation** - Pydantic schemas
- ✅ **Error Handling** - Clear, helpful messages
- ✅ **Business Rules** - Real-world logic enforced
- ✅ **Sample Data** - Ready to test immediately
- ✅ **Type Safety** - Full type hints
- ✅ **Production Ready** - Error handling, validation

## 📋 Sample Data Included

After running `python -m app.init_db`:
- 8 Books (various genres)
- 5 Members (some with active borrowings)
- 3 Borrowing records (including overdue)

## 🛠️ Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL ORM
- **SQLite** - Zero-config database
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## 💡 Example Use Cases

### Search Example
```bash
# Find all books related to "fantasy"
curl "http://localhost:8000/api/search/books?q=fantasy"
# Searches title, author, ISBN, and genre
```

### Statistics Example
```bash
# Get dashboard data
curl http://localhost:8000/api/stats/overview

# Response:
{
  "total_books": 8,
  "available_copies": 24,
  "active_members": 4,
  "overdue_borrowings": 1,
  "total_fines": 3.00
}
```

### Complete Workflow
```bash
# 1. Create member
curl -X POST http://localhost:8000/api/members \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com"}'

# 2. Search for a book
curl "http://localhost:8000/api/search/books?q=hobbit"

# 3. Borrow the book
curl -X POST http://localhost:8000/api/borrowings \
  -H "Content-Type: application/json" \
  -d '{"book_id":6,"member_id":1,"due_date":"2026-02-28"}'

# 4. Check statistics
curl http://localhost:8000/api/stats/overview
```

## 🎓 Learning Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pydantic**: https://docs.pydantic.dev/

## 🐛 Troubleshooting

**Port in use?**
```bash
uvicorn app.main:app --port 8080
```

**Database issues?**
```bash
rm library.db
python -m app.init_db
```

**Module not found?**
```bash
pip install -r requirements.txt
```

## 📞 Need Help?

1. Check **GETTING_STARTED.md** for detailed setup
2. Review **README.md** for API documentation
3. See **EXTRA_FEATURES.md** for bonus features
4. Try interactive docs at `/docs`

## 🎉 What Makes This Special?

1. **Minimal but Complete** - ~1,100 lines, full functionality
2. **2 Extra Features** - Search + Statistics (high value, low code)
3. **Production Quality** - Validation, error handling, docs
4. **Easy to Extend** - Clean architecture, modular design
5. **Well Documented** - 5 markdown guides included

## 🚀 Next Steps

1. ✅ Run the server: `python run.py`
2. ✅ Open Swagger UI: http://localhost:8000/docs
3. ✅ Try the search: http://localhost:8000/api/search/books?q=tolkien
4. ✅ Check statistics: http://localhost:8000/api/stats/overview
5. ✅ Read EXTRA_FEATURES.md for more details

**Enjoy building with the Library Management API!** 📚✨

