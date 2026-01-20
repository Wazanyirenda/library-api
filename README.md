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
# Development mode with auto-reload
python run.py

# Or using uvicorn directly
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

### Health Check
```
GET /health
```

### Books

| Method | Endpoint | Description | Query Parameters |
|--------|----------|-------------|------------------|
| GET | `/api/books` | Get all books | `genre`, `author`, `available` |
| GET | `/api/books/:id` | Get book by ID | - |
| GET | `/api/books/:id/availability` | Check book availability | - |
| POST | `/api/books` | Create new book | - |
| PUT | `/api/books/:id` | Update book | - |
| DELETE | `/api/books/:id` | Delete book | - |

#### Book Object
```json
{
  "title": "string (required, max 200)",
  "author": "string (required, max 100)",
  "isbn": "string (required, valid ISBN format)",
  "published_year": "integer (optional, 1000-current year)",
  "genre": "string (optional, max 50)",
  "total_copies": "integer (optional, default 1)",
  "available_copies": "integer (optional, default total_copies)"
}
```

#### Examples

**Get all books:**
```bash
curl http://localhost:8000/api/books
```

**Get available fiction books:**
```bash
curl "http://localhost:8000/api/books?genre=Fiction&available=true"
```

**Create a new book:**
```bash
curl -X POST http://localhost:8000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "isbn": "978-0-547-92822-7",
    "published_year": 1937,
    "genre": "Fantasy",
    "total_copies": 5,
    "available_copies": 5
  }'
```

**Update a book:**
```bash
curl -X PUT http://localhost:8000/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "978-0-7432-7356-5",
    "published_year": 1925,
    "genre": "Fiction",
    "total_copies": 4,
    "available_copies": 3
  }'
```

**Delete a book:**
```bash
curl -X DELETE http://localhost:8000/api/books/1
```

### Members

| Method | Endpoint | Description | Query Parameters |
|--------|----------|-------------|------------------|
| GET | `/api/members` | Get all members | `status`, `name` |
| GET | `/api/members/:id` | Get member by ID | - |
| GET | `/api/members/:id/history` | Get member's borrowing history | - |
| GET | `/api/members/:id/borrowings` | Get member's active borrowings | - |
| POST | `/api/members` | Create new member | - |
| PUT | `/api/members/:id` | Update member | - |
| DELETE | `/api/members/:id` | Delete member | - |

#### Member Object
```json
{
  "name": "string (required, max 100)",
  "email": "string (required, valid email)",
  "phone": "string (optional, phone format)",
  "address": "string (optional, max 200)",
  "status": "string (optional, default 'active', values: 'active'|'inactive'|'suspended')"
}
```

#### Examples

**Get all active members:**
```bash
curl "http://localhost:8000/api/members?status=active"
```

**Create a new member:**
```bash
curl -X POST http://localhost:8000/api/members \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Williams",
    "email": "alice@example.com",
    "phone": "555-0104",
    "address": "321 Elm St, City"
  }'
```

**Get member's borrowing history:**
```bash
curl http://localhost:8000/api/members/1/history
```

**Get member's active borrowings:**
```bash
curl http://localhost:8000/api/members/1/borrowings
```

### Borrowing Records

| Method | Endpoint | Description | Query Parameters |
|--------|----------|-------------|------------------|
| GET | `/api/borrowings` | Get all borrowing records | `status`, `member_id`, `book_id`, `overdue` |
| GET | `/api/borrowings/overdue` | Get overdue borrowings | - |
| GET | `/api/borrowings/:id` | Get borrowing record by ID | - |
| POST | `/api/borrowings` | Borrow a book | - |
| PUT | `/api/borrowings/:id/return` | Return a book | - |
| PUT | `/api/borrowings/:id/renew` | Renew a borrowing | - |

#### Borrowing Object
```json
{
  "book_id": "integer (required)",
  "member_id": "integer (required)",
  "due_date": "date (required, ISO8601 format, future date)"
}
```

#### Return Object
```json
{
  "fine_amount": "float (optional, auto-calculated if not provided)"
}
```

#### Renew Object
```json
{
  "new_due_date": "date (required, ISO8601 format, future date)"
}
```

#### Examples

**Borrow a book:**
```bash
curl -X POST http://localhost:8000/api/borrowings \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "member_id": 1,
    "due_date": "2026-02-15"
  }'
```

**Get all borrowed books:**
```bash
curl "http://localhost:8000/api/borrowings?status=borrowed"
```

**Get overdue borrowings:**
```bash
curl http://localhost:8000/api/borrowings/overdue
```

**Return a book:**
```bash
curl -X PUT http://localhost:8000/api/borrowings/1/return \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Return a book with custom fine:**
```bash
curl -X PUT http://localhost:8000/api/borrowings/1/return \
  -H "Content-Type: application/json" \
  -d '{
    "fine_amount": 5.00
  }'
```

**Renew a borrowing:**
```bash
curl -X PUT http://localhost:8000/api/borrowings/1/renew \
  -H "Content-Type: application/json" \
  -d '{
    "new_due_date": "2026-03-15"
  }'
```

## Business Rules

### Books
- ISBN must be unique
- Available copies cannot exceed total copies
- Cannot delete a book that is currently borrowed

### Members
- Email must be unique
- Only active members can borrow books
- Cannot delete a member with active borrowings

### Borrowings
- A member can only borrow one copy of the same book at a time
- Books must be available (available_copies > 0) to be borrowed
- Due date must be in the future
- Automatic fine calculation: $0.50 per day for overdue books
- Status automatically updated to 'overdue' when past due date

## Error Responses

The API returns consistent error responses:

```json
{
  "error": "Error message",
  "details": "Additional details (optional)"
}
```

### HTTP Status Codes

- `200 OK`: Successful GET request
- `201 Created`: Successful POST request
- `400 Bad Request`: Validation error or business rule violation
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Database Schema

### Books Table
```sql
- id: INTEGER PRIMARY KEY
- title: TEXT NOT NULL
- author: TEXT NOT NULL
- isbn: TEXT UNIQUE NOT NULL
- published_year: INTEGER
- genre: TEXT
- total_copies: INTEGER DEFAULT 1
- available_copies: INTEGER DEFAULT 1
- created_at: DATETIME
- updated_at: DATETIME
```

### Members Table
```sql
- id: INTEGER PRIMARY KEY
- name: TEXT NOT NULL
- email: TEXT UNIQUE NOT NULL
- phone: TEXT
- address: TEXT
- membership_date: DATE
- status: TEXT (active|inactive|suspended)
- created_at: DATETIME
- updated_at: DATETIME
```

### Borrowing Records Table
```sql
- id: INTEGER PRIMARY KEY
- book_id: INTEGER (FK to books)
- member_id: INTEGER (FK to members)
- borrow_date: DATE
- due_date: DATE NOT NULL
- return_date: DATE
- status: TEXT (borrowed|returned|overdue)
- fine_amount: REAL DEFAULT 0.0
- created_at: DATETIME
- updated_at: DATETIME
```

## Sample Data

The database initialization script includes sample data:

### Books
- The Great Gatsby by F. Scott Fitzgerald
- To Kill a Mockingbird by Harper Lee
- 1984 by George Orwell
- Pride and Prejudice by Jane Austen
- The Catcher in the Rye by J.D. Salinger

### Members
- John Doe (john.doe@example.com)
- Jane Smith (jane.smith@example.com)
- Bob Johnson (bob.johnson@example.com)

## Development

### Project Structure
```
library-api/
├── app/
│   ├── routers/
│   │   ├── __init__.py          # Routers package
│   │   ├── books.py             # Book endpoints
│   │   ├── members.py           # Member endpoints
│   │   └── borrowings.py        # Borrowing endpoints
│   ├── __init__.py              # App package
│   ├── database.py              # Database configuration
│   ├── models.py                # SQLAlchemy models
│   ├── schemas.py               # Pydantic schemas
│   ├── main.py                  # FastAPI application
│   └── init_db.py               # Database initialization script
├── .env                         # Environment variables
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore file
├── requirements.txt             # Python dependencies
├── run.py                       # Server entry point
└── README.md                    # This file
```

### Running the Application

**Development mode:**
```bash
python run.py
```

**Using uvicorn directly:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Initialize/Reset database:**
```bash
python -m app.init_db
```

## Testing the API

### Using Swagger UI (Recommended)

The easiest way to test the API is using the built-in Swagger UI:

1. Start the server: `python run.py`
2. Open your browser to http://localhost:8000/docs
3. Try out any endpoint directly from the interactive documentation

### Using curl

All examples in this README use curl for testing. See the examples above in each section.

### Using Postman

You can also use Postman or any other API client. Import the following endpoints:

1. Health Check: `GET /health`
2. Get All Books: `GET /api/books`
3. Create Book: `POST /api/books`
4. Get All Members: `GET /api/members`
5. Create Member: `POST /api/members`
6. Borrow Book: `POST /api/borrowings`
7. Return Book: `PUT /api/borrowings/:id/return`
8. Get Overdue: `GET /api/borrowings/overdue`

## Future Enhancements

- [ ] User authentication and authorization
- [ ] Book reservations
- [ ] Email notifications for due dates
- [ ] Search functionality with full-text search
- [ ] Pagination for large result sets
- [ ] Book categories and tags
- [ ] Multiple library branches support
- [ ] Digital book lending
- [ ] Member rating and review system
- [ ] Analytics and reporting

## License

MIT

## Author

Library Management API Team

## Support

For issues and questions, please open an issue on the repository.
