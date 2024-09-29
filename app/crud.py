from sqlalchemy.orm import Session

from app import models, schemas, utils


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.hash(password=user.password)
    db_user = models.User(name=user.name , email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_expense(db: Session, expense: schemas.ExpenseCreate, user_id: str):
    db_expense = models.Expense(**expense.model_dump(), user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Expense)
        .filter(models.Expense.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_expense(db: Session, expense_id: str, user_id: str):
    return (
        db.query(models.Expense)
        .filter(models.Expense.id == expense_id, models.Expense.user_id == user_id)
        .first()
    )


def delete_expense(db: Session, expense_id: str, user_id: str):
    expense = get_expense(db=db, expense_id=expense_id, user_id=user_id)
    if expense:
        db.delete(expense)
        db.commit()
        return True
    return False


def update_expense(
    db: Session, expense_id: str, expense: schemas.ExpenseCreate, user_id: str
):
    db_expense = get_expense(db=db, expense_id=expense_id, user_id=user_id)
    if db_expense:
        db_expense.tag = expense.tag
        db_expense.amount = expense.amount
        db_expense.description = expense.description
        db.commit()
        db.refresh(db_expense)
        return db_expense
    return None


def total_expense(db: Session, user_id: str):
    expenses = get_expenses(db=db, user_id=user_id)
    total = sum([expense.amount for expense in expenses])
    return total


def total_expense_by_tag(db: Session, tag: schemas.Tag, user_id: str):
    expenses = get_expenses(db=db, user_id=user_id)
    total = sum([expense.amount for expense in expenses if expense.tag == tag])
    return total
