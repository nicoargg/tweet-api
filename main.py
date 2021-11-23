#Python
from typing import Optional
from uuid import UUID
from datetime import date
from datetime import datetime

#Pydantic
from pydantic import BaseModel, EmailStr
from pydantic import Field

#FastApi
from fastapi import FastAPI


app = FastAPI()

# Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)


class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=58
        )


class User(UserBase):
    user_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    birth_date: Optional[date] = Field(default=None)


class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=280
        )
    created_at: datetime = Field(default=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)        
    by: User = Field(...)

@app.get(path="/",)
def home():
    return {"Twitter Api": "Working"}