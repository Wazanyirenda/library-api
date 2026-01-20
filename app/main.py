from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.database import engine, Base
from app.routers import books, members, borrowings, search, stats

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API",
    description="RESTful API for managing books, members, and borrowing records",
    version="1.0.0"
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [{"field": " -> ".join(str(x) for x in e["loc"]), "message": e["msg"]} 
              for e in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Validation error", "details": errors}
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Library API is running"}


app.include_router(books.router, prefix="/api")
app.include_router(members.router, prefix="/api")
app.include_router(borrowings.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(stats.router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": "Library Management API",
        "docs": "/docs",
        "health": "/health"
    }
