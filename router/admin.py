from fastapi import APIRouter,Depends, HTTPException,Path
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

from models import Todos
from database import SessionLocal
from .auth import get_current_user


router = APIRouter(
    prefix='/admin',
    tags=['admin']
);

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[Session,Depends(get_current_user)]

@router.get("/todos")
async def get_todos(user:user_dependency,db: db_dependency):
    print("->",user)
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication filed")
    if user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Not enough permissions")
    todos = db.query(Todos).all()
    return todos

## add api for delete todos by admin
@router.delete("/todo/{todo_id}/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(user:user_dependency,db: db_dependency,todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication filed")
    if user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Not enough permissions")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(todo_model)
    db.commit()
