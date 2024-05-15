# app/crud.py
from sqlalchemy import func
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).offset(skip).limit(limit).all()

def create_transaction(db: Session, transaction: schemas.TransactionCreate, user_id: int):
    db_transaction = models.Transaction(**transaction.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_summary(db: Session, user_id: int):
    income = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.user_id == user_id, models.Transaction.amount > 0).scalar() or 0
    expense = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.user_id == user_id, models.Transaction.amount < 0).scalar() or 0
    return {"income": income, "expense": expense, "balance": income + expense}
