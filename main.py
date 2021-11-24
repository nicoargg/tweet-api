#Python
import json
from typing import Optional, List
from uuid import UUID
from datetime import date
from datetime import datetime

#Pydantic
from pydantic import BaseModel, EmailStr
from pydantic import Field

#FastApi
from fastapi import FastAPI, status, Body, HTTPException, Path


app = FastAPI()

# Models

class UserBase(BaseModel):
    user_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    email: EmailStr = Field(...)


class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=58
    )


class User(UserBase):
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


class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=58
    )


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


#Functions
def read_files(files):
    with open(files, "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

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
def signup(user: UserRegister = Body(...)):
    """
    Signup

    Register an user in app

    Parameters:
        - Request body parameter:
            - user: UserRegister
    Returns a json with basic user information:
        - user_name: str
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_name"] = str(user_dict["user_name"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user

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
    """
    Show All Users

    Parameters:
        -
    Returns a json list with all users in the app with the following keys:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    read_files(files="users.json")

### Show an user
@app.get(
    path="/users/{user_name}",
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary="Show an user",
    tags=["Users"]
    )
def show_user(user_name: str = Path(
        ...,
        tittle = "User identificator",
        description = "It's an identificator for each user",
        example="nicorlas"
        )
):
    """
    Show a User

    This path operation show if a person exist in the app

    Parameters:
        - user_name: str

    Returns a json with user data:
        - user_name: str
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    results = read_files(files="users.json")
    id = str(user_name)
    for data in results:
        if data["user_name"] == id:
            return data
    else:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found :("
    )
    

### Delete an user
@app.delete(
    path="/users/{user_id}/delete",
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary="Delete an user",
    tags=["Users"]
    )
def delete_user(user_name: str = Path(
        ...,
        tittle = "Delete a User",
        description = "This delete an user",
        example="nicorlas"
        )
):
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
    """
    Show All Tweets

    Parameters:
        -
    Returns a json list with all tweets in the app with the following keys:
        tweet_id: UUID
        content: str
        created_at: datetime
        updated_at: Optional[datetime] 
        by: User
    """
    read_files(files="tweets.json")


### Post a tweet
@app.post(
    path="/post",
    response_model= Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
    )
def post(tweet: Tweet = Body(...)):
    """
    Post a tweet

    Post a tweet in the app

    Parameters:
        - Request body parameter:
            - tweet: Tweet
    Returns a json with basic tweet information:
        tweet_id: UUID
        content: str
        created_at: datetime
        updated_at: Optional[datetime] 
        by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_name"] = str(tweet_dict["by"]["user_name"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])

        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet

### Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model= Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
    )
def show_a_tweet(tweet_id: UUID = Path(
        ...,
        tittle = "Tweet identificator",
        description = "It's an identificator for each tweet",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
        )
):
    id = str(tweet_id)
    results = read_files(files="tweets.json")
    for data in results:
        if data["tweet_id"] == id:
            return data
        else:
            raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Tweet not found :("
        )


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
def update_a_tweet(tweet: Tweet = Body(...)):
    pass