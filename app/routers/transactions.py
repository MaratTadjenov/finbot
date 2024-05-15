# app/routers/transactions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..dependencies import get_db

router = APIRouter()

@router.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_transaction(db=db, transaction=transaction, user_id=user_id)

@router.get("/transactions/", response_model=List[schemas.Transaction])
def read_transactions(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    transactions = crud.get_transactions(db, user_id=user_id, skip=skip, limit=limit)
    return transactions
