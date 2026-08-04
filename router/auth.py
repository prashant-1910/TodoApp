from datetime import timedelta, datetime,timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from RequestDTO.UserRequest import UserRequest
from ResponseDTO.Token import Token
#from models import Users
from Models.User import Users
from database import SessionLocal

router = APIRouter(
    prefix='/auth',
    tags=['auth']
);

SECRET_KEY = "KJASKBSKFBSBAKBAKBKBAKBAKBKKFHDSKJFDBSBKDSDSKDSFKSKAKSA"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

oath2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db : db_dependency,
                      userRequest: UserRequest):
    user_model = Users(username=userRequest.username, email=userRequest.email,
                      hashed_password=bcrypt_context.hash(userRequest.password),
                      first_name=userRequest.firstName, last_name=userRequest.lastName, role=userRequest.role,
                      is_active=True)
    db.add(user_model)
    db.commit()
    return True

@router.get("/users",status_code=status.HTTP_200_OK)
async def get_users(db : db_dependency):
    users = db.query(Users).all()
    return users

@router.post("/token",response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],db: db_dependency):
    print("Generating access token")
    user = authenticated_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials")
    token = create_access_token(user.username, user.id, timedelta(minutes=10),user.role)
    access_token = Token(access_token = token,token_type="bearer")
    print("Token : ",token)
    return access_token

def authenticated_user(db ,username,password):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username:str,user_id:int,expires_timedelta:timedelta,role:str):
    expires = datetime.now(timezone.utc) + expires_timedelta
    encode = {'sub': username,'id': user_id,'exp': expires,"role": role}
    #encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token:Annotated[str,Depends(oath2_bearer)]):
    print("Validating token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload['sub']
        user_id: int = payload['id']
        user_role: str = payload['role']
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials 1")
        return {'username':username,'user_id':user_id,'user_role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials 2")
