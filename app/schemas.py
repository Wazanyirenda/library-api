from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: str = Field(..., min_length=10, max_length=20)
    published_year: Optional[int] = Field(None, ge=1000, le=datetime.now().year)
    genre: Optional[str] = Field(None, max_length=50)
    total_copies: int = Field(1, ge=1)
    available_copies: int = Field(1, ge=0)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, min_length=10, max_length=20)
    published_year: Optional[int] = Field(None, ge=1000, le=datetime.now().year)
    genre: Optional[str] = Field(None, max_length=50)
    total_copies: Optional[int] = Field(None, ge=1)
    available_copies: Optional[int] = Field(None, ge=0)


class Book(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MemberBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=3, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=200)
    status: str = Field("active")


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, min_length=3, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=200)
    status: Optional[str] = None


class Member(MemberBase):
    id: int
    membership_date: date
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BorrowingBase(BaseModel):
    book_id: int = Field(..., gt=0)
    member_id: int = Field(..., gt=0)
    due_date: date

    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, v: date) -> date:
        if v <= date.today():
            raise ValueError('Due date must be in the future')
        return v


class BorrowingCreate(BorrowingBase):
    pass


class BorrowingReturn(BaseModel):
    fine_amount: Optional[float] = Field(None, ge=0)


class BorrowingRenew(BaseModel):
    new_due_date: date

    @field_validator('new_due_date')
    @classmethod
    def validate_date(cls, v: date) -> date:
        if v <= date.today():
            raise ValueError('New due date must be in the future')
        return v


class Borrowing(BaseModel):
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


class BorrowingWithDetails(Borrowing):
    book: Book
    member: Member

    class Config:
        from_attributes = True
