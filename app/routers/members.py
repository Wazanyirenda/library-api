from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Member as MemberModel, BorrowingRecord
from app.schemas import Member, MemberCreate, MemberUpdate, BorrowingWithDetails

router = APIRouter(prefix="/members", tags=["Members"])


@router.get("/", response_model=List[Member])
def get_members(
    status_filter: Optional[str] = Query(None, alias="status"),
    name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(MemberModel)
    if status_filter:
        query = query.filter(MemberModel.status == status_filter)
    if name:
        query = query.filter(MemberModel.name.ilike(f"%{name}%"))
    return query.all()


@router.get("/{member_id}", response_model=Member)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(MemberModel).filter(MemberModel.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail=f"Member {member_id} not found")
    return member


@router.get("/{member_id}/history", response_model=List[BorrowingWithDetails])
def get_member_history(member_id: int, db: Session = Depends(get_db)):
    if not db.query(MemberModel).filter(MemberModel.id == member_id).first():
        raise HTTPException(status_code=404, detail=f"Member {member_id} not found")
    return db.query(BorrowingRecord).filter(BorrowingRecord.member_id == member_id).all()


@router.get("/{member_id}/borrowings", response_model=List[BorrowingWithDetails])
def get_member_borrowings(member_id: int, db: Session = Depends(get_db)):
    if not db.query(MemberModel).filter(MemberModel.id == member_id).first():
        raise HTTPException(status_code=404, detail=f"Member {member_id} not found")
    return db.query(BorrowingRecord).filter(
        BorrowingRecord.member_id == member_id,
        BorrowingRecord.status.in_(["borrowed", "overdue"])
    ).all()


@router.post("/", response_model=Member, status_code=status.HTTP_201_CREATED)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    if db.query(MemberModel).filter(MemberModel.email == member.email).first():
        raise HTTPException(status_code=400, detail=f"Email {member.email} already exists")
    
    db_member = MemberModel(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.put("/{member_id}", response_model=Member)
def update_member(member_id: int, member_update: MemberUpdate, db: Session = Depends(get_db)):
    db_member = db.query(MemberModel).filter(MemberModel.id == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail=f"Member {member_id} not found")
    
    if member_update.email and member_update.email != db_member.email:
        if db.query(MemberModel).filter(MemberModel.email == member_update.email).first():
            raise HTTPException(status_code=400, detail=f"Email {member_update.email} already exists")
    
    update_data = member_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_member, field, value)
    
    db.commit()
    db.refresh(db_member)
    return db_member


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(MemberModel).filter(MemberModel.id == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail=f"Member {member_id} not found")
    
    if db.query(BorrowingRecord).filter(
        BorrowingRecord.member_id == member_id,
        BorrowingRecord.status.in_(["borrowed", "overdue"])
    ).first():
        raise HTTPException(status_code=400, detail="Cannot delete member with active borrowings")
    
    db.delete(db_member)
    db.commit()
