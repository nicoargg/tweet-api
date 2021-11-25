#Python
import json
from typing import Optional, List
from uuid import UUID
from datetime import date
from datetime import datetime
from fastapi.param_functions import Query

#Pydantic
from pydantic import BaseModel, EmailStr
from pydantic import Field

#FastApi
from fastapi import FastAPI, status, Body, HTTPException, Path, Form



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
def read_file(entity: str):
    with open(entity + ".json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

def search_id(id, results, dict_key: str):
    id = str(id)
    for data in results:
        if data[dict_key] == id:
            return data, True
    else:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail= dict_key + " not found :("
    )

def insert_to_file(entity: str, body_parameter):
    with open(entity + ".json", "r+", encoding='utf-8') as f:
        results = json.loads(f.read()) # cast str -> json
        json_dict = body_parameter.dict()
        
        if entity == "tweets":
            json_dict["tweet_id"] = str(json_dict["tweet_id"]) # manual cast / fastapi can't cast uuid automatically
            json_dict["created_at"] = str(json_dict["created_at"]) # manual cast / fastapi can't cast date automatically

            if len(str(json_dict["updated_at"])) > 0 :
                json_dict["updated_at"] = str(json_dict["updated_at"]) # manual cast / fastapi can't cast date automatically
            json_dict["by"]["user_name"] = str(json_dict["by"]["user_name"])
            json_dict["by"]["birth_date"] = str(json_dict["by"]["birth_date"])

        else:
            json_dict['user_name'] = str(json_dict['user_name'])
            json_dict['birth_date'] = str(json_dict['birth_date'])
        
        results.append(json_dict)
        f.seek(0) # start writing at the beginning like overwrite
        f.write(json.dumps(results))

def overwrite_file(entity: str, result_list):
    with open(entity + '.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(result_list))

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

    insert_to_file(entity="users",body_parameter=user)
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
    pass #working on this

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
    return read_file(entity="users")

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
    results = read_file(entity="users")
    user,found =search_id(user_name, results, dict_key="user_name")
    return user
    

### Delete an user
@app.delete(
    path="/users/{user_name}/delete",
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
    """
    Delete a User

    This path operation delete a user in the app

    Parameters:
        - user_name: str

    Returns a json with deleted user data:
        - user_name: user_name
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    results = read_file(entity="users")
    user ,found = search_id(user_name, results, dict_key="user_name")
    if found:
        results.remove(user)
        overwrite_file(entity="users", result_list=results)
        return user


### Update an User
@app.put(
    path="/users/{user_name}/update",
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary="Update an user",
    tags=["Users"]
    )
def update_user(user_name: str = Path(
        ...,
        tittle = "Delete a User",
        description = "This delete an user",
        example="nicorlas"
        ),    
    first_name: Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=50,
        title="First name",
        description="This is the first name of the user, minimum characters: 1"
    ),
    last_name: Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=50,
        title="Last name",
        description="This is the last name of the user, minimum characters: 1"
    ),
    email: Optional[EmailStr] = Query(
        default=None,
        title="Email",
        description="This is the email of the user")
):
    """
     Update a user
    This path operation Update a user

     Parameters:
    - path parameter:
        - user_name: str
    - query parameters:
        - first_name: str
        - last_name: str
        -email: EmailStr
    
     Returns a json list with the following keys
    - user_name: str
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birthday: date
    """
    results= read_file(entity="users")
    user,found=search_id(user_name,results,dict_key="user_name")
    if found:
        if first_name:
            user["first_name"] = first_name
        if last_name:
            user["last_name"] = last_name
        if email:
            user["email"] = email
        overwrite_file(entity='users', result_list=results)
        return user



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
    return read_file(entity="tweets")


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
    insert_to_file(entity="tweets",body_parameter=tweet)
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
    """
     Show a tweet
    this path parameter show a tweet of the app by the tweet_id (UUID)
     Parameters:
    - path parameter
        - tweet_id: str
    
     Returns a json with the basic tweet information (tweet model):
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: datetime
    - by: user
    """
    results = read_file(entity="tweets")
    tweet,found=search_id(tweet_id, results, dict_key="tweet_id")
    return tweet

### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model= Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
    )
def delete_a_tweet(tweet_id: UUID = Path(
        ...,
        tittle = "Tweet identificator",
        description = "It's an identificator for each tweet",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
        )
):
    """
     Delete a tweet
    This path operation delete a tweet from a json
    ## Parameters:
    - path parameter:
        - tweet_id: str
    
    ## Returns a json list with the following keys
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: datetime
    - by: user
    """
    results = read_file(entity="tweets")
    tweet ,found = search_id(tweet_id, results, dict_key="tweet_id")
    if found:
        results.remove(tweet)
        overwrite_file(entity="tweets", result_list=results)
        return tweet

### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model= Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
    )
def update_a_tweet(
    tweet_id = Path(
    ...,
    title='tweet id',
    description="this is the tweet id. Minimum characters: 1"
    ),
    content: Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=280,
        title="Tweet content",
        description="This is content of the tweet, minimum characters: 1"
    )
):
    """
     Update a tweet
    This path operation Update a tweet
    ## Parameters:
    - path parameter:
        - tweet_id: str
    - query parameters:
        - content: str
    
     Returns a json list following keys
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: datetime
    - by: user
    """
    results= read_file(entity="tweets")
    tweet,found=search_id(tweet_id,results,dict_key="tweet_id")
    if found:
        if content:
            tweet["content"]=content
    overwrite_file(entity='tweets', result_list=results)
    return tweet