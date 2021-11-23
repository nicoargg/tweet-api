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


class UserRegister(UserBase, UserLogin):
    pass

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
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)        
    by: User = Field(...)

#Path Operations


##Users

### Register User
@app.post(
    path="/signup",
    response_model= User,
    status_code=status.HTTP_201_CREATED,
    summary="Register an user",
    tags=["Users"]
    )
def signup():
    """
    Signup

    Register an user in app

    Parameters:
        - Request body parameter:
            - user: UserRegister
    Returns a json with basic user information:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
    """


### Login
@app.post(
    path="/login",
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary="Login an user",
    tags=["Users"]
    )
def login():
    pass

### Show all users
@app.get(
    path="/users",
    response_model= List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
    )
def show_all_users():
    pass

### Show an user
@app.get(
    path="/users/{user_id}",
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary="Show an user",
    tags=["Users"]
    )
def show_user():
    pass

### Delete an user
@app.delete(
    path="/users/{user_id}/delete",
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary="Delete an user",
    tags=["Users"]
    )
def delete_user():
    pass

### Update an User
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

###Show all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
    )
def home():
    return {"Twitter Api": "Working"}

### Post a tweet
@app.post(
    path="/post",
    response_model= Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
    )
def post():
    pass

### Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model= Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
    )
def show_a_tweet():
    pass

### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model= Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
    )
def delete_a_tweet():
    pass

### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model= Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
    )
def update_a_tweet():
    pass