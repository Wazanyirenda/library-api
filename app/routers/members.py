from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Member as MemberModel, BorrowingRecord
from app.schemas import Member, MemberCreate, MemberUpdate, BorrowingRecordWithDetails

router = APIRouter(prefix="/members", tags=["Members"])


@router.get("/", response_model=List[Member], summary="Get all members")
def get_members(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status (active, inactive, suspended)"),
    name: Optional[str] = Query(None, description="Filter by name (partial match)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all library members with optional filters.
    
    - **status**: Filter members by status (active, inactive, suspended)
    - **name**: Filter members by name (partial match)
    - **skip**: Pagination offset
    - **limit**: Maximum number of results (default 100, max 100)
    """
    query = db.query(MemberModel)
    
    if status_filter:
        if status_filter not in ["active", "inactive", "suspended"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status must be one of: active, inactive, suspended"
            )
        query = query.filter(MemberModel.status == status_filter)
    
    if name:
        query = query.filter(MemberModel.name.ilike(f"%{name}%"))
    
    members = query.offset(skip).limit(limit).all()
    return members


@router.get("/{member_id}", response_model=Member, summary="Get member by ID")
def get_member(member_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific member by their ID.
    
    - **member_id**: The ID of the member to retrieve
    """
    member = db.query(MemberModel).filter(MemberModel.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {member_id} not found"
        )
    return member


@router.get("/{member_id}/history", response_model=List[BorrowingRecordWithDetails], summary="Get member's borrowing history")
def get_member_history(
    member_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get the complete borrowing history for a specific member.
    
    - **member_id**: The ID of the member
    - **skip**: Pagination offset
    - **limit**: Maximum number of results
    """
    # Check if member exists
    member = db.query(MemberModel).filter(MemberModel.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {member_id} not found"
        )
    
    borrowings = db.query(BorrowingRecord).filter(
        BorrowingRecord.member_id == member_id
    ).order_by(BorrowingRecord.borrow_date.desc()).offset(skip).limit(limit).all()
    
    return borrowings


@router.get("/{member_id}/borrowings", response_model=List[BorrowingRecordWithDetails], summary="Get member's active borrowings")
def get_member_active_borrowings(member_id: int, db: Session = Depends(get_db)):
    """
    Get all currently active (not returned) borrowings for a specific member.
    
    - **member_id**: The ID of the member
    """
    # Check if member exists
    member = db.query(MemberModel).filter(MemberModel.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {member_id} not found"
        )
    
    active_borrowings = db.query(BorrowingRecord).filter(
        BorrowingRecord.member_id == member_id,
        BorrowingRecord.status.in_(["borrowed", "overdue"])
    ).all()
    
    return active_borrowings


@router.post("/", response_model=Member, status_code=status.HTTP_201_CREATED, summary="Create a new member")
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    """
    Register a new library member.
    
    - **name**: Name of the member (required)
    - **email**: Email address (required, must be unique)
    - **phone**: Phone number (optional)
    - **address**: Address (optional)
    - **status**: Membership status (default: active)
    """
    # Check if email already exists
    existing_member = db.query(MemberModel).filter(MemberModel.email == member.email).first()
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Member with email {member.email} already exists"
        )
    
    db_member = MemberModel(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.put("/{member_id}", response_model=Member, summary="Update a member")
def update_member(member_id: int, member_update: MemberUpdate, db: Session = Depends(get_db)):
    """
    Update an existing member's information.
    
    - **member_id**: The ID of the member to update
    - All fields are optional; only provided fields will be updated
    """
    db_member = db.query(MemberModel).filter(MemberModel.id == member_id).first()
    if not db_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {member_id} not found"
        )
    
    # Check if email is being updated and if it already exists
    if member_update.email and member_update.email != db_member.email:
        existing_member = db.query(MemberModel).filter(MemberModel.email == member_update.email).first()
        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Member with email {member_update.email} already exists"
            )
    
    # Update only provided fields
    update_data = member_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_member, field, value)
    
    db.commit()
    db.refresh(db_member)
    return db_member


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a member")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    """
    Delete a member from the library system.
    
    - **member_id**: The ID of the member to delete
    - Cannot delete a member with active borrowings
    """
    db_member = db.query(MemberModel).filter(MemberModel.id == member_id).first()
    if not db_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {member_id} not found"
        )
    
    # Check if member has active borrowings
    active_borrowings = db.query(BorrowingRecord).filter(
        BorrowingRecord.member_id == member_id,
        BorrowingRecord.status.in_(["borrowed", "overdue"])
    ).first()
    
    if active_borrowings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a member with active borrowings"
        )
    
    db.delete(db_member)
    db.commit()
    return None

