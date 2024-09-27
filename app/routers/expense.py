from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas, crud, oauth2
from app.database import get_db

router = APIRouter(prefix="/expense", tags=["Expenses"])


@router.post("", response_model=schemas.Expense)
def create_expense(
    expense: schemas.ExpenseBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    return crud.create_expense(db=db, expense=expense, user_id=current_user.id)


@router.get("", response_model=list[schemas.Expense])
def read_expenses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    expenses = crud.get_expenses(db=db, skip=skip, limit=limit, user_id=current_user.id)
    return expenses


@router.get("/{expense_id}", response_model=schemas.Expense)
def read_expense(
    expense_id: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    expense = crud.get_expense(db=db, expense_id=expense_id, user_id=current_user.id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.delete("/{expense_id}")
def delete_expense(
    expense_id: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    expense = crud.get_expense(db=db, expense_id=expense_id, user_id=current_user.id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}


@router.put("/{expense_id}", response_model=schemas.Expense)
def update_expense(
    expense_id: str,
    expense: schemas.ExpenseBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    db_expense = crud.get_expense(db=db, expense_id=expense_id, user_id=current_user.id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db_expense.tag = expense.tag
    db_expense.amount = expense.amount
    db_expense.description = expense.description
    db.commit()
    db.refresh(db_expense)
    return db_expense