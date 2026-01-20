from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine, Base
from app.routers import books, members, borrowings, search, stats

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Book Management API",
    description="""
    A comprehensive RESTful API for managing books, members, and borrowing records in a library system.
    
    ## Features
    
    * **Book Management**: Create, read, update, and delete books
    * **Member Management**: Manage library members and their accounts
    * **Borrowing System**: Track book borrowings, returns, and due dates
    * **Advanced Search**: Unified search across books by title, author, ISBN, or genre
    * **Statistics Dashboard**: Real-time library analytics and popular books tracking
    * **Validation**: Comprehensive input validation for all endpoints
    * **Error Handling**: Meaningful error messages and proper HTTP status codes
    * **Filters**: Query parameters for filtering and searching
    * **Overdue Tracking**: Automatic tracking and fine calculation for overdue books
    
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
    """,
    version="1.0.0",
    contact={
        "name": "Library Management API",
        "url": "https://github.com/yourusername/library-api",
    },
    license_info={
        "name": "MIT",
    },
)


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors with detailed messages.
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation error",
            "details": errors
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Handle database errors.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Database error",
            "details": str(exc)
        }
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {
        "status": "healthy",
        "message": "Library Management API is running",
        "version": "1.0.0"
    }


# Include routers
app.include_router(books.router, prefix="/api")
app.include_router(members.router, prefix="/api")
app.include_router(borrowings.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(stats.router, prefix="/api")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Welcome to the Library Management API",
        "version": "1.0.0",
        "documentation": "/docs",
        "openapi": "/openapi.json"
    }

