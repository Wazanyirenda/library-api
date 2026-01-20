# Library Management API - FastAPI Examples

This file contains comprehensive examples for testing all API endpoints.

## Base URL
```
http://localhost:8000
```

## Table of Contents
- [Health Check](#health-check)
- [Books API](#books-api)
- [Members API](#members-api)
- [Borrowing Records API](#borrowing-records-api)

---

## Health Check

### Check API Health
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Library Management API is running",
  "version": "1.0.0"
}
```

---

## Books API

### 1. Get All Books
```bash
curl http://localhost:8000/api/books
```

### 2. Get Books with Filters
```bash
# Get all Fiction books
curl "http://localhost:8000/api/books?genre=Fiction"

# Get all available books
curl "http://localhost:8000/api/books?available=true"

# Get books by author
curl "http://localhost:8000/api/books?author=Tolkien"

# Combine filters
curl "http://localhost:8000/api/books?genre=Fantasy&available=true"

# With pagination
curl "http://localhost:8000/api/books?skip=0&limit=10"
```

### 3. Get Single Book
```bash
curl http://localhost:8000/api/books/1
```

### 4. Check Book Availability
```bash
curl http://localhost:8000/api/books/1/availability
```

**Response:**
```json
{
  "book_id": 1,
  "title": "The Great Gatsby",
  "available_copies": 3,
  "total_copies": 3,
  "is_available": true
}
```

### 5. Create a Book
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

### 6. Update a Book
```bash
# Full update
curl -X PUT http://localhost:8000/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby - Updated",
    "author": "F. Scott Fitzgerald",
    "isbn": "978-0-7432-7356-5",
    "published_year": 1925,
    "genre": "Classic Fiction",
    "total_copies": 4,
    "available_copies": 3
  }'

# Partial update (only update specific fields)
curl -X PUT http://localhost:8000/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{
    "total_copies": 5,
    "available_copies": 4
  }'
```

### 7. Delete a Book
```bash
curl -X DELETE http://localhost:8000/api/books/1
```

---

## Members API

### 1. Get All Members
```bash
curl http://localhost:8000/api/members
```

### 2. Get Members with Filters
```bash
# Get active members
curl "http://localhost:8000/api/members?status=active"

# Search by name
curl "http://localhost:8000/api/members?name=John"

# With pagination
curl "http://localhost:8000/api/members?skip=0&limit=10"
```

### 3. Get Single Member
```bash
curl http://localhost:8000/api/members/1
```

### 4. Get Member's Borrowing History
```bash
curl http://localhost:8000/api/members/1/history
```

### 5. Get Member's Active Borrowings
```bash
curl http://localhost:8000/api/members/1/borrowings
```

### 6. Create a Member
```bash
curl -X POST http://localhost:8000/api/members \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Williams",
    "email": "alice.williams@example.com",
    "phone": "555-0104",
    "address": "321 Elm St, City",
    "status": "active"
  }'
```

### 7. Update a Member
```bash
# Full update
curl -X PUT http://localhost:8000/api/members/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe Updated",
    "email": "john.doe@example.com",
    "phone": "555-0199",
    "address": "123 Main St, New City",
    "status": "active"
  }'

# Partial update
curl -X PUT http://localhost:8000/api/members/1 \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "555-0199",
    "address": "123 Main St, New City"
  }'
```

### 8. Delete a Member
```bash
curl -X DELETE http://localhost:8000/api/members/1
```

---

## Borrowing Records API

### 1. Get All Borrowing Records
```bash
curl http://localhost:8000/api/borrowings
```

### 2. Get Borrowings with Filters
```bash
# Get borrowed books (currently out)
curl "http://localhost:8000/api/borrowings?status=borrowed"

# Get returned books
curl "http://localhost:8000/api/borrowings?status=returned"

# Get overdue books
curl "http://localhost:8000/api/borrowings?status=overdue"

# Get borrowings for a specific member
curl "http://localhost:8000/api/borrowings?member_id=1"

# Get borrowings for a specific book
curl "http://localhost:8000/api/borrowings?book_id=1"

# Filter by overdue status
curl "http://localhost:8000/api/borrowings?overdue=true"

# With pagination
curl "http://localhost:8000/api/borrowings?skip=0&limit=10"
```

### 3. Get Overdue Borrowings
```bash
curl http://localhost:8000/api/borrowings/overdue
```

### 4. Get Single Borrowing Record
```bash
curl http://localhost:8000/api/borrowings/1
```

### 5. Borrow a Book
```bash
curl -X POST http://localhost:8000/api/borrowings \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "member_id": 1,
    "due_date": "2026-02-28"
  }'
```

**Response:**
```json
{
  "id": 1,
  "book_id": 1,
  "member_id": 1,
  "borrow_date": "2026-01-20",
  "due_date": "2026-02-28",
  "return_date": null,
  "status": "borrowed",
  "fine_amount": 0.0,
  "created_at": "2026-01-20T10:30:00",
  "updated_at": "2026-01-20T10:30:00"
}
```

### 6. Return a Book
```bash
# Return with auto-calculated fine
curl -X PUT http://localhost:8000/api/borrowings/1/return \
  -H "Content-Type: application/json" \
  -d '{}'

# Return with custom fine amount
curl -X PUT http://localhost:8000/api/borrowings/1/return \
  -H "Content-Type: application/json" \
  -d '{
    "fine_amount": 5.00
  }'
```

**Response:**
```json
{
  "id": 1,
  "book_id": 1,
  "member_id": 1,
  "borrow_date": "2026-01-20",
  "due_date": "2026-02-28",
  "return_date": "2026-03-05",
  "status": "returned",
  "fine_amount": 2.50,
  "created_at": "2026-01-20T10:30:00",
  "updated_at": "2026-03-05T14:20:00"
}
```

### 7. Renew a Borrowing
```bash
curl -X PUT http://localhost:8000/api/borrowings/1/renew \
  -H "Content-Type: application/json" \
  -d '{
    "new_due_date": "2026-03-31"
  }'
```

---

## Error Examples

### 1. Book Not Found
```bash
curl http://localhost:8000/api/books/9999
```

**Response (404):**
```json
{
  "detail": "Book with id 9999 not found"
}
```

### 2. Validation Error
```bash
curl -X POST http://localhost:8000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "",
    "author": "Test Author",
    "isbn": "123"
  }'
```

**Response (422):**
```json
{
  "error": "Validation error",
  "details": [
    {
      "field": "body -> title",
      "message": "String should have at least 1 character",
      "type": "string_too_short"
    },
    {
      "field": "body -> isbn",
      "message": "ISBN must be 10 or 13 digits",
      "type": "value_error"
    }
  ]
}
```

### 3. Business Rule Violation
```bash
# Try to borrow a book that's not available
curl -X POST http://localhost:8000/api/borrowings \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "member_id": 1,
    "due_date": "2026-02-28"
  }'
```

**Response (400):**
```json
{
  "detail": "Book 'The Great Gatsby' is not available (no copies available)"
}
```

### 4. Duplicate Email
```bash
curl -X POST http://localhost:8000/api/members \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "john.doe@example.com"
  }'
```

**Response (400):**
```json
{
  "detail": "Member with email john.doe@example.com already exists"
}
```

---

## Python Examples

### Using requests library

```python
import requests
import json
from datetime import date, timedelta

BASE_URL = "http://localhost:8000"

# Get all books
response = requests.get(f"{BASE_URL}/api/books")
books = response.json()
print(f"Total books: {len(books)}")

# Create a new book
new_book = {
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "isbn": "978-0-13-235088-4",
    "published_year": 2008,
    "genre": "Programming",
    "total_copies": 3,
    "available_copies": 3
}
response = requests.post(f"{BASE_URL}/api/books", json=new_book)
print(f"Created book: {response.json()}")

# Create a new member
new_member = {
    "name": "Alice Johnson",
    "email": "alice.j@example.com",
    "phone": "555-0200",
    "status": "active"
}
response = requests.post(f"{BASE_URL}/api/members", json=new_member)
member = response.json()
print(f"Created member: {member}")

# Borrow a book
borrowing = {
    "book_id": 1,
    "member_id": member["id"],
    "due_date": str(date.today() + timedelta(days=14))
}
response = requests.post(f"{BASE_URL}/api/borrowings", json=borrowing)
print(f"Borrowed book: {response.json()}")

# Get member's active borrowings
response = requests.get(f"{BASE_URL}/api/members/{member['id']}/borrowings")
active_borrowings = response.json()
print(f"Active borrowings: {len(active_borrowings)}")

# Return a book
borrowing_id = active_borrowings[0]["id"]
response = requests.put(f"{BASE_URL}/api/borrowings/{borrowing_id}/return", json={})
print(f"Returned book: {response.json()}")
```

---

## Testing Workflow

### Complete Borrowing Workflow

```bash
# 1. Create a member
curl -X POST http://localhost:8000/api/members \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "555-0999"
  }'
# Note the member ID from response

# 2. Check book availability
curl http://localhost:8000/api/books/1/availability

# 3. Borrow the book
curl -X POST http://localhost:8000/api/borrowings \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "member_id": 6,
    "due_date": "2026-02-28"
  }'
# Note the borrowing ID from response

# 4. Check book availability again (should decrease)
curl http://localhost:8000/api/books/1/availability

# 5. View member's active borrowings
curl http://localhost:8000/api/members/6/borrowings

# 6. Renew the borrowing
curl -X PUT http://localhost:8000/api/borrowings/4/renew \
  -H "Content-Type: application/json" \
  -d '{
    "new_due_date": "2026-03-31"
  }'

# 7. Return the book
curl -X PUT http://localhost:8000/api/borrowings/4/return \
  -H "Content-Type: application/json" \
  -d '{}'

# 8. Check book availability (should increase)
curl http://localhost:8000/api/books/1/availability

# 9. View member's borrowing history
curl http://localhost:8000/api/members/6/history
```

---

## Advanced Queries

### Pagination Example
```bash
# Get first page of books (10 items)
curl "http://localhost:8000/api/books?skip=0&limit=10"

# Get second page
curl "http://localhost:8000/api/books?skip=10&limit=10"
```

### Complex Filtering
```bash
# Get all overdue borrowings for a specific member
curl "http://localhost:8000/api/borrowings?member_id=1&status=overdue"

# Get all available Fantasy books
curl "http://localhost:8000/api/books?genre=Fantasy&available=true"
```

### Batch Operations
```bash
# Get statistics
TOTAL_BOOKS=$(curl -s http://localhost:8000/api/books | jq 'length')
TOTAL_MEMBERS=$(curl -s http://localhost:8000/api/members | jq 'length')
OVERDUE=$(curl -s http://localhost:8000/api/borrowings/overdue | jq 'length')

echo "Total Books: $TOTAL_BOOKS"
echo "Total Members: $TOTAL_MEMBERS"
echo "Overdue Borrowings: $OVERDUE"
```

