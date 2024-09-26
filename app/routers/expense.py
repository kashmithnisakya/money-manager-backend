from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas, crud, oauth2
from app.database import get_db

router = APIRouter(prefix="/expense", tags=["Expenses"])

@router.post("", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return crud.create_expense(db=db, expense=expense, user_id=current_user.id)