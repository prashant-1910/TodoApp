from pydantic import BaseModel, Field

class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    completed: bool
    priority: int = Field(gt=0, lt=10)
