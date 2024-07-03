from typing import Annotated, Sequence
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import  OAuth2PasswordRequestForm
from models.user_models import (User, UserREQ, TokenRES, UserUpdateFirstName, UserUpdateLastName, UserUpdateUsername, UserUpdateEmail, UserUpdatePassword, UserUpdatePhoneNumber)
from db.settings import DB_SESSION
from auth_controllers.user_controller import(get_all_user_data, get_login_user, update_user_first_name, update_user_last_name, update_user_username, update_user_email, update_user_password, update_user_phone_number, deleted_users)
from kafka.kafka import create_users_in_kafka


user_router: APIRouter = APIRouter()

@user_router.get("/")
def hello_user():
    return {"message": "Hello User"}


@user_router.get("/all_users/", response_model=list[User], status_code=status.HTTP_200_OK)
def get_all_users_data(db: DB_SESSION):
   data:Sequence[User] = get_all_user_data(db = db)
   return data

@user_router.post("/signup/", response_model=User, status_code=status.HTTP_201_CREATED)
async def add_users(users:Annotated[UserREQ, Depends(create_users_in_kafka)]):
    if not users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="some thing went wrong adding user in kafka or database")
    return users

@user_router.post("/login/", response_model=TokenRES, status_code=status.HTTP_200_OK)
def login_users(login:Annotated[OAuth2PasswordRequestForm, Depends(get_login_user)]):
    if not login:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Auth Faild")
    return login


# This Will Update User and user can update own

@user_router.put("/update_user_first_name/", response_model = UserUpdateFirstName, status_code = status.HTTP_200_OK)
def updated_users_first_name(db: DB_SESSION, user_id: int, updated_users_first_name: UserUpdateFirstName):
    return update_user_first_name(db = db, user_id = user_id, first_name = updated_users_first_name.updated_first_name)

@user_router.put("/update_user_last_name/", response_model = UserUpdateLastName, status_code = status.HTTP_200_OK)
def updated_users_last_name(db: DB_SESSION, user_id: int, updated_users_last_name: UserUpdateLastName):
    return update_user_last_name(db = db, user_id = user_id, last_name = updated_users_last_name.updated_last_name)

@user_router.put("/update_user_username/", response_model = UserUpdateUsername, status_code = status.HTTP_200_OK)
def updated_users_username(db: DB_SESSION, user_id: int, updated_users_username: UserUpdateUsername):
    return update_user_username(db = db, user_id = user_id, username = updated_users_username.updated_username)

@user_router.put("/update_user_email/", response_model = UserUpdateEmail, status_code = status.HTTP_200_OK)
def updated_users_email(db: DB_SESSION, user_id: int, updated_users_email: UserUpdateEmail):
    return update_user_email(db = db, user_id = user_id, email = updated_users_email.updated_email)

@user_router.put("/update_user_password/", response_model = UserUpdatePassword, status_code = status.HTTP_200_OK)
def updated_users_password(db: DB_SESSION, user_id: int, updated_password: UserUpdatePassword):
    return update_user_password(db = db, user_id = user_id, old_password = updated_password.old_password, updated_new_password = updated_password.updated_new_password)

@user_router.put("/update_user_phone_number/", response_model = UserUpdatePhoneNumber, status_code = status.HTTP_200_OK)
def updated_users_phone_number(db: DB_SESSION, user_id: int, updated_users_phone_number: UserUpdatePhoneNumber):
    return update_user_phone_number(db = db, user_id = user_id, phone_number = updated_users_phone_number.updated_phone_number)


# We will decide later user can also be delete their account and also admin have rights to delete his account too

@user_router.delete("/delete_user/", status_code = status.HTTP_200_OK)
def delete_users(db: DB_SESSION, user_id: int):
    return deleted_users(db = db, user_id = user_id)