#Python
from typing import Optional, List
from uuid import UUID
from datetime import date
from datetime import datetime

#Pydantic
from pydantic import BaseModel, EmailStr
from pydantic import Field

#FastApi
from fastapi import FastAPI, status


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

#Path Operations

@app.get(path="/",)
def home():
    return {"Twitter Api": "Working"}

##Users
@app.post(
    path="/signup",
    response_model= User,
    status_code=status.HTTP_201_CREATED,
    summary="Register an user",
    tags=["Users"]
    )
def signup():
    pass


@app.post(
    path="/login",
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary="Login an user",
    tags=["Users"]
    )
def login():
    pass

@app.get(
    path="/users",
    response_model= List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
    )
def show_all_users():
    pass

@app.get(
    path="/users/{user_id}",
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary="Show an user",
    tags=["Users"]
    )
def show_user():
    pass

@app.delete(
    path="/users/{user_id}/delete",
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary="Delete an user",
    tags=["Users"]
    )
def delete_user():
    pass

@app.put(
    path="/users/{user_id}/update",
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary="Update an user",
    tags=["Users"]
    )
def update_user():
    pass


##Tweets
