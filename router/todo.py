from fastapi import APIRouter,Depends, HTTPException,Path
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
import models
from models import Todos
from database import SessionLocal
from .auth import get_current_user


router = APIRouter(
    tags=["todo"]
);

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[Session,Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3,max_length=100)
    description: str = Field(min_length=3,max_length=100)
    completed: bool
    priority: int = Field(gt=0,lt=10)

@router.get("/todo/",status_code=status.HTTP_200_OK)
async def read_all_todos(user:user_dependency,db: db_dependency):
    return db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()

@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def get_todo_by_id(user:user_dependency,db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication filed")
    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id')).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=404, detail="Todo Not found")

@router.post("/todo",status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,
                      db:db_dependency,todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication filed")
    todo_model = models.Todos(**todo_request.model_dump(),owner_id=user.get('user_id'))
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model

@router.put("/todo/{todo_id}/",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo_by_id(user:user_dependency,db: db_dependency,todo_request: TodoRequest,
                            todo_id: int = Path(gt=0)
                            ):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication filed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Not found")
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.completed = todo_request.completed
    todo_model.priority = todo_request.priority
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

@router.delete("/todo/{todo_id}/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(user:user_dependency,db: db_dependency,todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication filed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(todo_model)
    db.commit()
