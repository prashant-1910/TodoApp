from fastapi import APIRouter, Depends, HTTPException, Path, Body
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from Models.Todos import Todos
from RequestDTO.TodoRequest import TodoRequest
from database import SessionLocal
from .auth import get_current_user
from service.TodoService import TodoService


router = APIRouter(
    tags=["todo"]
);

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]


@router.get("/todo/",status_code=status.HTTP_200_OK)
async def read_all_todos(user:user_dependency,db: db_dependency):
    return TodoService.get_all_todos(db,user.get('user_id'))

@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def get_todo_by_id(user:user_dependency,db: db_dependency, todo_id: int = Path(gt=0)):
    return TodoService.get_todo_by_id(db, user.get('user_id'), todo_id)

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,db: db_dependency, todo_request: TodoRequest):
    return TodoService.create_todo(db, todo_request, user.get('user_id'))


@router.put("/todo/{todo_id}/")
async def update_todo_by_id(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0),
    todo_request: TodoRequest = Body(...)
):
    return TodoService.update_todo(db, todo_request, user.get('user_id'), todo_id)

@router.delete("/todo/{todo_id}/")
async def delete_todo_by_id(user:user_dependency,db: db_dependency,todo_id: int = Path(gt=0)):
    return TodoService.delete_todo(db,user.get('user_id'), todo_id)
