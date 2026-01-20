# Library API - Quick Start Examples

## Setup and Start

```bash
# Install dependencies
npm install

# Initialize database with sample data
npm run init-db

# Start the server
npm run dev
```

## Quick Test Commands

### Health Check
```bash
curl http://localhost:3000/health
```

### API Info
```bash
curl http://localhost:3000/api
```

## Books Endpoints

### 1. Get All Books
```bash
curl http://localhost:3000/api/books
```

### 2. Get Books by Genre
```bash
curl "http://localhost:3000/api/books?genre=Fiction"
```

### 3. Get Available Books Only
```bash
curl "http://localhost:3000/api/books?available=true"
```

### 4. Get Specific Book
```bash
curl http://localhost:3000/api/books/1
```

### 5. Check Book Availability
```bash
curl http://localhost:3000/api/books/1/availability
```

### 6. Create New Book
```bash
curl -X POST http://localhost:3000/api/books \
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

### 7. Update Book
```bash
curl -X PUT http://localhost:3000/api/books/1 \
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

## Members Endpoints

### 1. Get All Members
```bash
curl http://localhost:3000/api/members
```

### 2. Get Active Members
```bash
curl "http://localhost:3000/api/members?status=active"
```

### 3. Get Specific Member
```bash
curl http://localhost:3000/api/members/1
```

### 4. Create New Member
```bash
curl -X POST http://localhost:3000/api/members \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Williams",
    "email": "alice@example.com",
    "phone": "555-0104",
    "address": "321 Elm St, City"
  }'
```

### 5. Get Member's Borrowing History
```bash
curl http://localhost:3000/api/members/1/history
```

### 6. Get Member's Active Borrowings
```bash
curl http://localhost:3000/api/members/1/borrowings
```

### 7. Update Member
```bash
curl -X PUT http://localhost:3000/api/members/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe Updated",
    "email": "john.doe@example.com",
    "phone": "555-0101",
    "address": "123 Main St, City",
    "status": "active"
  }'
```

## Borrowing Endpoints

### 1. Get All Borrowing Records
```bash
curl http://localhost:3000/api/borrowings
```

### 2. Get Borrowed Books
```bash
curl "http://localhost:3000/api/borrowings?status=borrowed"
```

### 3. Get Overdue Books
```bash
curl http://localhost:3000/api/borrowings/overdue
```

### 4. Borrow a Book
```bash
curl -X POST http://localhost:3000/api/borrowings \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "member_id": 1,
    "due_date": "2024-03-01"
  }'
```

### 5. Return a Book (Auto-calculate Fine)
```bash
curl -X PUT http://localhost:3000/api/borrowings/1/return \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 6. Return a Book with Custom Fine
```bash
curl -X PUT http://localhost:3000/api/borrowings/1/return \
  -H "Content-Type: application/json" \
  -d '{
    "fine_amount": 5.00
  }'
```

### 7. Renew a Borrowing
```bash
curl -X PUT http://localhost:3000/api/borrowings/1/renew \
  -H "Content-Type: application/json" \
  -d '{
    "new_due_date": "2024-04-01"
  }'
```

### 8. Get Borrowings by Member
```bash
curl "http://localhost:3000/api/borrowings?member_id=1"
```

### 9. Get Borrowings by Book
```bash
curl "http://localhost:3000/api/borrowings?book_id=1"
```

## Complete Workflow Example

### 1. Create a New Member
```bash
curl -X POST http://localhost:3000/api/members \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "555-9999",
    "address": "Test Address"
  }'
# Note the returned memberId
```

### 2. Add a New Book
```bash
curl -X POST http://localhost:3000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Book",
    "author": "Test Author",
    "isbn": "978-0-123-45678-9",
    "published_year": 2024,
    "genre": "Test",
    "total_copies": 1,
    "available_copies": 1
  }'
# Note the returned bookId
```

### 3. Borrow the Book
```bash
# Use the IDs from steps 1 and 2
curl -X POST http://localhost:3000/api/borrowings \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 6,
    "member_id": 4,
    "due_date": "2024-03-01"
  }'
# Note the returned borrowingId
```

### 4. Check Book Availability
```bash
curl http://localhost:3000/api/books/6/availability
# Should show available_copies: 0
```

### 5. Return the Book
```bash
# Use the borrowingId from step 3
curl -X PUT http://localhost:3000/api/borrowings/1/return \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 6. Verify Availability Restored
```bash
curl http://localhost:3000/api/books/6/availability
# Should show available_copies: 1
```

## Testing Error Handling

### 1. Borrow Unavailable Book
```bash
# First borrow all copies, then try to borrow again
curl -X POST http://localhost:3000/api/borrowings \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "member_id": 1,
    "due_date": "2024-03-01"
  }'
```

### 2. Create Duplicate ISBN
```bash
curl -X POST http://localhost:3000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Duplicate Book",
    "author": "Test Author",
    "isbn": "978-0-7432-7356-5",
    "published_year": 2024,
    "genre": "Test",
    "total_copies": 1
  }'
# Should return error: ISBN already exists
```

### 3. Create Duplicate Email
```bash
curl -X POST http://localhost:3000/api/members \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Duplicate User",
    "email": "john.doe@example.com",
    "phone": "555-0000"
  }'
# Should return error: Email already exists
```

### 4. Invalid Due Date (Past Date)
```bash
curl -X POST http://localhost:3000/api/borrowings \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "member_id": 1,
    "due_date": "2020-01-01"
  }'
# Should return validation error
```

### 5. Borrow Same Book Twice
```bash
# Borrow a book
curl -X POST http://localhost:3000/api/borrowings \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 2,
    "member_id": 1,
    "due_date": "2024-03-01"
  }'

# Try to borrow same book again
curl -X POST http://localhost:3000/api/borrowings \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 2,
    "member_id": 1,
    "due_date": "2024-03-01"
  }'
# Should return error: Already has active borrowing
```

## Tips for Testing

1. **Use a REST client** like Postman, Insomnia, or Thunder Client for easier testing
2. **Check the database** after operations to verify changes
3. **Test validation** by sending invalid data
4. **Test edge cases** like borrowing all copies, returning already returned books
5. **Monitor the console** for helpful log messages
6. **Use the health check** to verify the server is running

## Common Response Formats

### Success Response (GET)
```json
{
  "count": 5,
  "books": [...]
}
```

### Success Response (POST)
```json
{
  "message": "Book created successfully",
  "bookId": 6
}
```

### Error Response
```json
{
  "error": "Book not found"
}
```

### Validation Error Response
```json
{
  "errors": [
    {
      "msg": "Title is required",
      "param": "title",
      "location": "body"
    }
  ]
}
```

