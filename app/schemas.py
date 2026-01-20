from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime, date
from typing import Optional, Literal
import re


# ==================== Book Schemas ====================

class BookBase(BaseModel):
    """Base schema for Book with common fields."""
    title: str = Field(..., min_length=1, max_length=200, description="Title of the book")
    author: str = Field(..., min_length=1, max_length=100, description="Author of the book")
    isbn: str = Field(..., min_length=10, max_length=20, description="ISBN of the book")
    published_year: Optional[int] = Field(None, ge=1000, le=datetime.now().year, description="Year the book was published")
    genre: Optional[str] = Field(None, max_length=50, description="Genre of the book")
    total_copies: int = Field(1, ge=1, description="Total number of copies")
    available_copies: int = Field(1, ge=0, description="Number of available copies")

    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v: str) -> str:
        """Validate ISBN format (ISBN-10 or ISBN-13)."""
        # Remove hyphens and spaces
        isbn = re.sub(r'[\s-]', '', v)
        if len(isbn) not in [10, 13]:
            raise ValueError('ISBN must be 10 or 13 digits')
        if not isbn.replace('-', '').replace(' ', '').replace('X', '').isdigit():
            raise ValueError('ISBN must contain only digits (and optionally X for ISBN-10)')
        return v

    @field_validator('available_copies')
    @classmethod
    def validate_available_copies(cls, v: int, info) -> int:
        """Ensure available copies don't exceed total copies."""
        if 'total_copies' in info.data and v > info.data['total_copies']:
            raise ValueError('Available copies cannot exceed total copies')
        return v


class BookCreate(BookBase):
    """Schema for creating a new book."""
    pass


class BookUpdate(BaseModel):
    """Schema for updating a book (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, min_length=10, max_length=20)
    published_year: Optional[int] = Field(None, ge=1000, le=datetime.now().year)
    genre: Optional[str] = Field(None, max_length=50)
    total_copies: Optional[int] = Field(None, ge=1)
    available_copies: Optional[int] = Field(None, ge=0)

    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v: Optional[str]) -> Optional[str]:
        """Validate ISBN format if provided."""
        if v is None:
            return v
        isbn = re.sub(r'[\s-]', '', v)
        if len(isbn) not in [10, 13]:
            raise ValueError('ISBN must be 10 or 13 digits')
        return v


class Book(BookBase):
    """Schema for returning book data."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookAvailability(BaseModel):
    """Schema for book availability information."""
    book_id: int
    title: str
    available_copies: int
    total_copies: int
    is_available: bool

    class Config:
        from_attributes = True


# ==================== Member Schemas ====================

class MemberBase(BaseModel):
    """Base schema for Member with common fields."""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the member")
    email: EmailStr = Field(..., description="Email address of the member")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    address: Optional[str] = Field(None, max_length=200, description="Address")
    status: Literal["active", "inactive", "suspended"] = Field("active", description="Membership status")

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format."""
        if v is None:
            return v
        # Remove common phone separators
        phone = re.sub(r'[\s\-\(\)\.]', '', v)
        if not phone.isdigit():
            raise ValueError('Phone number must contain only digits and separators')
        if len(phone) < 10 or len(phone) > 15:
            raise ValueError('Phone number must be between 10 and 15 digits')
        return v


class MemberCreate(MemberBase):
    """Schema for creating a new member."""
    pass


class MemberUpdate(BaseModel):
    """Schema for updating a member (all fields optional)."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=200)
    status: Optional[Literal["active", "inactive", "suspended"]] = None

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format if provided."""
        if v is None:
            return v
        phone = re.sub(r'[\s\-\(\)\.]', '', v)
        if not phone.isdigit():
            raise ValueError('Phone number must contain only digits and separators')
        if len(phone) < 10 or len(phone) > 15:
            raise ValueError('Phone number must be between 10 and 15 digits')
        return v


class Member(MemberBase):
    """Schema for returning member data."""
    id: int
    membership_date: date
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Borrowing Record Schemas ====================

class BorrowingRecordBase(BaseModel):
    """Base schema for BorrowingRecord with common fields."""
    book_id: int = Field(..., gt=0, description="ID of the book being borrowed")
    member_id: int = Field(..., gt=0, description="ID of the member borrowing the book")
    due_date: date = Field(..., description="Due date for returning the book")

    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, v: date) -> date:
        """Ensure due date is in the future."""
        if v <= date.today():
            raise ValueError('Due date must be in the future')
        return v


class BorrowingRecordCreate(BorrowingRecordBase):
    """Schema for creating a new borrowing record."""
    pass


class BorrowingRecordReturn(BaseModel):
    """Schema for returning a book."""
    fine_amount: Optional[float] = Field(None, ge=0, description="Fine amount (auto-calculated if not provided)")


class BorrowingRecordRenew(BaseModel):
    """Schema for renewing a borrowing."""
    new_due_date: date = Field(..., description="New due date for the book")

    @field_validator('new_due_date')
    @classmethod
    def validate_new_due_date(cls, v: date) -> date:
        """Ensure new due date is in the future."""
        if v <= date.today():
            raise ValueError('New due date must be in the future')
        return v


class BorrowingRecord(BaseModel):
    """Schema for returning borrowing record data."""
    id: int
    book_id: int
    member_id: int
    borrow_date: date
    due_date: date
    return_date: Optional[date]
    status: str
    fine_amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BorrowingRecordWithDetails(BorrowingRecord):
    """Schema for returning borrowing record with book and member details."""
    book: Book
    member: Member

    class Config:
        from_attributes = True


# ==================== Response Schemas ====================

class ErrorResponse(BaseModel):
    """Schema for error responses."""
    error: str
    details: Optional[str] = None


class SuccessResponse(BaseModel):
    """Schema for success responses."""
    message: str
    data: Optional[dict] = None

