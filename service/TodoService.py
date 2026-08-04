from typing import List

from narwhals import Boolean
from sqlalchemy.orm import Session
from fastapi import HTTPException

from RequestDTO.TodoRequest import TodoRequest
from Models.Todos import Todos
from pydantic import BaseModel, Field


class TodoService:
    @staticmethod
    def create_todo(db: Session, todo_request: TodoRequest, user_id: int) -> Todos:
        """
        Create a new todo for the authenticated user.
        
        Args:
            db: Database session
            todo_request: Todo request data
            user_id: ID of the authenticated user
            
        Returns:
            The created Todos model instance
            
        Raises:
            HTTPException: If user is not authenticated
        """
        if user_id is None:
            raise HTTPException(status_code=401, detail="Authentication failed while creating TODO")
        
        todo_model = Todos(
            **todo_request.model_dump(),
            owner_id=user_id
        )
        db.add(todo_model)
        db.commit()
        db.refresh(todo_model)
        return todo_model

    @staticmethod
    def update_todo(db: Session, todo_request: TodoRequest, user_id: int, todo_id: int) -> bool:
        print("In update_todo")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Authentication filed")

        todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user_id).first()
        if todo_model is None:
            raise HTTPException(status_code=404, detail="Not found")
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.completed = todo_request.completed
        todo_model.priority = todo_request.priority
        db.add(todo_model)
        db.commit()
        db.refresh(todo_model)
        return True

    @staticmethod
    def delete_todo(db: Session, user_id: int, todo_id: int) -> bool:
        if user_id is None:
            raise HTTPException(status_code=401, detail="Authentication filed")

        todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user_id).first()
        if todo_model is None:
            raise HTTPException(status_code=404, detail="Not found")
        db.delete(todo_model)
        db.commit()
        return True

    @staticmethod
    def get_all_todos(db: Session, user_id: int) -> List[Todos]:
        return db.query(Todos).filter(Todos.owner_id == user_id).all()

    @staticmethod
    def get_todo_by_id(db: Session, user_id: int, todo_id: int) -> Todos:
        if user_id is None:
            raise HTTPException(status_code=401, detail="Authentication filed")
        todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user_id).first()
        if todo is not None:
            return todo
        raise HTTPException(status_code=404, detail="Todo Not found")