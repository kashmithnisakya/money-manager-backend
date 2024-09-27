from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas, crud, oauth2
from app.database import get_db

router = APIRouter(tags=["Process"])


@router.get("/total", response_model=float)
def total_expense(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    print(current_user)
    expenses = crud.get_expenses(db=db, user_id=current_user.id)
    total = sum([expense.amount for expense in expenses])
    return total


@router.get("/total/{tag}", response_model=float)
def total_expense_by_tag(
    tag: schemas.Tag,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    expenses = crud.get_expenses(db=db, user_id=current_user.id)
    total = sum([expense.amount for expense in expenses if expense.tag == tag])
    return total


# create report for total expenses by tag
@router.get("/report", response_model=dict)
def total_expense_report(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    expenses = crud.get_expenses(db=db, user_id=current_user.id)
    tags = schemas.Tag
    report = {
        tag: sum([expense.amount for expense in expenses if expense.tag == tag])
        for tag in tags
    }
    return report
