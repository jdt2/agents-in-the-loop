from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Todo title")
    completed: bool = Field(default=False, description="Completion status")

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class TodoResponse(TodoBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime