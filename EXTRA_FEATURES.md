# Extra Features Documentation

This document describes the additional features implemented in the Library Management API.

## 1. Advanced Search 🔍

**Endpoint:** `GET /api/search/books`

### Description
Unified search functionality that searches across multiple book fields (title, author, ISBN, and genre) with a single query parameter.

### Parameters
- `q` (required): Search query string
- `limit` (optional): Maximum results (default: 20, max: 100)

### Examples

**Search for books by author:**
```bash
curl "http://localhost:8000/api/search/books?q=tolkien"
```

**Search for books by title:**
```bash
curl "http://localhost:8000/api/search/books?q=gatsby"
```

**Search by ISBN:**
```bash
curl "http://localhost:8000/api/search/books?q=978-0-547"
```

**Search by genre:**
```bash
curl "http://localhost:8000/api/search/books?q=fantasy&limit=5"
```

### Response Example
```json
[
  {
    "id": 6,
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "isbn": "978-0-547-92822-7",
    "published_year": 1937,
    "genre": "Fantasy",
    "total_copies": 4,
    "available_copies": 3,
    "created_at": "2026-01-20T10:00:00",
    "updated_at": "2026-01-20T10:00:00"
  }
]
```

### Benefits
- **Convenience**: Search across all fields with one query
- **Fast**: Case-insensitive pattern matching
- **Flexible**: Works with partial matches
- **User-friendly**: Simple query parameter interface

---

## 2. Statistics Dashboard 📊

### 2.1 Library Overview

**Endpoint:** `GET /api/stats/overview`

### Description
Provides comprehensive library statistics including books, members, borrowings, and financial metrics.

### Example
```bash
curl http://localhost:8000/api/stats/overview
```

### Response
```json
{
  "total_books": 8,
  "total_copies": 27,
  "available_copies": 24,
  "total_members": 5,
  "active_members": 4,
  "total_borrowings": 15,
  "active_borrowings": 2,
  "overdue_borrowings": 1,
  "total_fines": 12.50
}
```

### Metrics Explained
- `total_books`: Unique book titles in the library
- `total_copies`: Sum of all physical copies
- `available_copies`: Copies currently available for borrowing
- `total_members`: All registered members
- `active_members`: Members with "active" status
- `total_borrowings`: All-time borrowing records
- `active_borrowings`: Currently borrowed books (not returned)
- `overdue_borrowings`: Books past their due date
- `total_fines`: Sum of all fines collected

### Use Cases
- Dashboard displays
- Reports generation
- System health monitoring
- Admin overview

---

### 2.2 Popular Books

**Endpoint:** `GET /api/stats/popular-books`

### Description
Returns the most frequently borrowed books, useful for understanding patron preferences and making acquisition decisions.

### Parameters
- `limit` (optional): Number of top books to return (default: 10)

### Example
```bash
curl "http://localhost:8000/api/stats/popular-books?limit=5"
```

### Response
```json
[
  {
    "book_id": 7,
    "title": "Harry Potter and the Philosopher's Stone",
    "author": "J.K. Rowling",
    "borrow_count": 12
  },
  {
    "book_id": 3,
    "title": "1984",
    "author": "George Orwell",
    "borrow_count": 8
  },
  {
    "book_id": 6,
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "borrow_count": 7
  }
]
```

### Use Cases
- Identify popular books for more copies
- Collection development insights
- Marketing and promotion decisions
- Display trending books to users

---

## Python Usage Examples

### Search Integration
```python
import requests

BASE_URL = "http://localhost:8000"

# Search for fantasy books
response = requests.get(f"{BASE_URL}/api/search/books", params={"q": "fantasy"})
books = response.json()
print(f"Found {len(books)} fantasy books")

# Search with limit
response = requests.get(
    f"{BASE_URL}/api/search/books",
    params={"q": "tolkien", "limit": 3}
)
for book in response.json():
    print(f"- {book['title']} by {book['author']}")
```

### Statistics Integration
```python
import requests

BASE_URL = "http://localhost:8000"

# Get library overview
response = requests.get(f"{BASE_URL}/api/stats/overview")
stats = response.json()

print(f"Library Statistics:")
print(f"  Total Books: {stats['total_books']}")
print(f"  Available Copies: {stats['available_copies']}/{stats['total_copies']}")
print(f"  Active Members: {stats['active_members']}/{stats['total_members']}")
print(f"  Overdue Books: {stats['overdue_borrowings']}")
print(f"  Total Fines: ${stats['total_fines']:.2f}")

# Get popular books
response = requests.get(f"{BASE_URL}/api/stats/popular-books", params={"limit": 5})
popular = response.json()

print("\nTop 5 Most Borrowed Books:")
for i, book in enumerate(popular, 1):
    print(f"  {i}. {book['title']} - {book['borrow_count']} times")
```

### Building a Dashboard
```python
import requests
from datetime import date

def get_dashboard_data():
    """Fetch all data needed for a library dashboard."""
    base_url = "http://localhost:8000"
    
    # Get statistics
    stats = requests.get(f"{base_url}/api/stats/overview").json()
    
    # Get popular books
    popular = requests.get(f"{base_url}/api/stats/popular-books", params={"limit": 5}).json()
    
    # Get overdue borrowings
    overdue = requests.get(f"{base_url}/api/borrowings/overdue").json()
    
    return {
        "stats": stats,
        "popular_books": popular,
        "overdue_borrowings": overdue,
        "generated_at": date.today().isoformat()
    }

# Use in your application
dashboard = get_dashboard_data()
print(f"Dashboard generated at: {dashboard['generated_at']}")
```

---

## Testing the Features

### Quick Test Script

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "=== Testing Search Feature ==="
echo "Searching for 'tolkien'..."
curl -s "$BASE_URL/api/search/books?q=tolkien" | jq '.[].title'

echo -e "\n=== Testing Statistics ==="
echo "Getting library overview..."
curl -s "$BASE_URL/api/stats/overview" | jq '.'

echo -e "\nGetting popular books..."
curl -s "$BASE_URL/api/stats/popular-books?limit=3" | jq '.[]'
```

Save as `test_features.sh`, make executable (`chmod +x test_features.sh`), and run.

---

## Performance Notes

### Search
- Uses indexed columns for fast lookups
- Case-insensitive search using ILIKE
- Limited results to prevent performance issues
- Searches across 4 fields: title, author, ISBN, genre

### Statistics
- Aggregation queries optimized with SQLAlchemy
- Minimal joins for better performance
- Cached results recommended for production use
- Overdue status updated on-the-fly

---

## Future Enhancements

While keeping the codebase minimal, these could be added:

1. **Search Improvements**
   - Search history
   - Search suggestions/autocomplete
   - Relevance scoring

2. **Statistics Enhancements**
   - Time-based statistics (monthly/yearly trends)
   - Member borrowing statistics
   - Genre popularity analysis
   - Export to CSV/PDF

3. **Additional Features**
   - Book reservations
   - Reading recommendations
   - Member activity feed

---

## Summary

These two extra features significantly enhance the Library Management API:

✅ **Search**: Provides quick, unified search across all book fields
✅ **Statistics**: Delivers actionable insights for library management

Both features are:
- Minimal code additions
- High-value functionality
- RESTful and well-documented
- Production-ready
- Easy to test and use

