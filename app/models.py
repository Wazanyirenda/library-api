from sqlalchemy import Column, Integer, String, DateTime, Date, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Book(Base):
    """
    Book model representing books in the library.
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(100), nullable=False, index=True)
    isbn = Column(String(30), unique=True, nullable=False, index=True)
    published_year = Column(Integer, nullable=True)
    genre = Column(String(50), nullable=True, index=True)
    total_copies = Column(Integer, default=1, nullable=False)
    available_copies = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    borrowing_records = relationship("BorrowingRecord", back_populates="book")

    __table_args__ = (
        CheckConstraint('available_copies >= 0', name='check_available_copies_positive'),
        CheckConstraint('total_copies >= 0', name='check_total_copies_positive'),
        CheckConstraint('available_copies <= total_copies', name='check_available_lte_total'),
    )


class Member(Base):
    """
    Member model representing library members.
    """
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(200), nullable=True)
    membership_date = Column(Date, default=datetime.utcnow().date, nullable=False)
    status = Column(String(20), default="active", nullable=False, index=True)  # active, inactive, suspended
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    borrowing_records = relationship("BorrowingRecord", back_populates="member")


class BorrowingRecord(Base):
    """
    BorrowingRecord model representing book borrowing transactions.
    """
    __tablename__ = "borrowing_records"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="RESTRICT"), nullable=False, index=True)
    member_id = Column(Integer, ForeignKey("members.id", ondelete="RESTRICT"), nullable=False, index=True)
    borrow_date = Column(Date, default=datetime.utcnow().date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    status = Column(String(20), default="borrowed", nullable=False, index=True)  # borrowed, returned, overdue
    fine_amount = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    book = relationship("Book", back_populates="borrowing_records")
    member = relationship("Member", back_populates="borrowing_records")

    __table_args__ = (
        CheckConstraint('fine_amount >= 0', name='check_fine_positive'),
    )

