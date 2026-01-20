"""
Database initialization script with sample data.
Run this script to populate the database with sample books and members.
"""

from datetime import date, timedelta
from app.database import SessionLocal, engine, Base
from app.models import Book, Member, BorrowingRecord


def init_database():
    """
    Initialize the database with tables and sample data.
    """
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Book).first() is not None:
            print("Database already contains data. Skipping initialization.")
            return
        
        print("Adding sample books...")
        books = [
            Book(
                title="The Great Gatsby",
                author="F. Scott Fitzgerald",
                isbn="978-0-7432-7356-5",
                published_year=1925,
                genre="Fiction",
                total_copies=3,
                available_copies=3
            ),
            Book(
                title="To Kill a Mockingbird",
                author="Harper Lee",
                isbn="978-0-06-112008-4",
                published_year=1960,
                genre="Fiction",
                total_copies=4,
                available_copies=4
            ),
            Book(
                title="1984",
                author="George Orwell",
                isbn="978-0-452-28423-4",
                published_year=1949,
                genre="Science Fiction",
                total_copies=5,
                available_copies=5
            ),
            Book(
                title="Pride and Prejudice",
                author="Jane Austen",
                isbn="978-0-14-143951-8",
                published_year=1813,
                genre="Romance",
                total_copies=2,
                available_copies=2
            ),
            Book(
                title="The Catcher in the Rye",
                author="J.D. Salinger",
                isbn="978-0-316-76948-0",
                published_year=1951,
                genre="Fiction",
                total_copies=3,
                available_copies=3
            ),
            Book(
                title="The Hobbit",
                author="J.R.R. Tolkien",
                isbn="978-0-547-92822-7",
                published_year=1937,
                genre="Fantasy",
                total_copies=4,
                available_copies=3
            ),
            Book(
                title="Harry Potter and the Philosopher's Stone",
                author="J.K. Rowling",
                isbn="978-0-439-70818-8",
                published_year=1997,
                genre="Fantasy",
                total_copies=6,
                available_copies=5
            ),
            Book(
                title="The Lord of the Rings",
                author="J.R.R. Tolkien",
                isbn="978-0-618-64561-1",
                published_year=1954,
                genre="Fantasy",
                total_copies=3,
                available_copies=2
            ),
        ]
        
        db.add_all(books)
        db.commit()
        print(f"Added {len(books)} books.")
        
        print("Adding sample members...")
        members = [
            Member(
                name="John Doe",
                email="john.doe@example.com",
                phone="555-0101",
                address="123 Main St, City",
                status="active"
            ),
            Member(
                name="Jane Smith",
                email="jane.smith@example.com",
                phone="555-0102",
                address="456 Oak Ave, City",
                status="active"
            ),
            Member(
                name="Bob Johnson",
                email="bob.johnson@example.com",
                phone="555-0103",
                address="789 Pine Rd, City",
                status="active"
            ),
            Member(
                name="Alice Williams",
                email="alice.williams@example.com",
                phone="555-0104",
                address="321 Elm St, City",
                status="active"
            ),
            Member(
                name="Charlie Brown",
                email="charlie.brown@example.com",
                phone="555-0105",
                address="654 Maple Dr, City",
                status="inactive"
            ),
        ]
        
        db.add_all(members)
        db.commit()
        print(f"Added {len(members)} members.")
        
        print("Adding sample borrowing records...")
        # Create some sample borrowing records
        borrowings = [
            BorrowingRecord(
                book_id=6,  # The Hobbit
                member_id=1,  # John Doe
                borrow_date=date.today() - timedelta(days=5),
                due_date=date.today() + timedelta(days=9),
                status="borrowed"
            ),
            BorrowingRecord(
                book_id=7,  # Harry Potter
                member_id=2,  # Jane Smith
                borrow_date=date.today() - timedelta(days=3),
                due_date=date.today() + timedelta(days=11),
                status="borrowed"
            ),
            BorrowingRecord(
                book_id=8,  # Lord of the Rings
                member_id=3,  # Bob Johnson
                borrow_date=date.today() - timedelta(days=20),
                due_date=date.today() - timedelta(days=6),
                status="overdue",
                fine_amount=3.0
            ),
        ]
        
        db.add_all(borrowings)
        db.commit()
        print(f"Added {len(borrowings)} borrowing records.")
        
        print("\n✅ Database initialized successfully!")
        print(f"   - {len(books)} books")
        print(f"   - {len(members)} members")
        print(f"   - {len(borrowings)} borrowing records")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()

