from fastapi import APIRouter,Depends, HTTPException,Path
from typing import Annotated

from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from Models.User import Users
from starlette import status
from database import SessionLocal
from RequestDTO.UserVerified import userVarification
from .auth import get_current_user


router = APIRouter(
    prefix='/user',
    tags=['user']
);


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[Session,Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/")
async def get_user_info(user:user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication filed")
    user = db.query(Users).filter(Users.id == user.get('user_id')).first()
    return user

@router.put("/password",status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user:user_dependency,db: db_dependency,user_verification:userVarification):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication filed")
    user_model = db.query(Users).filter(Users.id == user.get('user_id')).first()

    if not bcrypt_context.verify(user_verification.password,user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect Password")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
