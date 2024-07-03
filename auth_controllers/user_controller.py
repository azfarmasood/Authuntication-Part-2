from typing import Sequence
from sqlmodel import Session, select
from models.user_models import User, UserREQ, LoginREQ
from fastapi import HTTPException
from sqlmodel import select
from security.strictnes import (create_access_token, hash_password, verify_password, strong_password, phone_number_strict, strict_email_methods, strict_username_methods, strict_first_name, strict_last_name)
from db.settings import access_token, DB_SESSION


def get_all_user_data(db: DB_SESSION):
    all_users:Sequence[User] = db.exec(select(User)).all()
    return all_users


async def create_users_in_db(user: UserREQ, db: Session):
    create_user: User = User(**user.__dict__)
    create_user.password =  hash_password(user.password)
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return create_user


# This Will Login User With Correct Credentials:

def get_login_user(data: LoginREQ, db: DB_SESSION):
    user: User | None =  db.exec(select(User).where(User.username == data.username)).first()
    
    """
    This Will Can Only Be Usable When User Creates Cutome RequestForm OR Custome OAuth2RequestForm This logic will only available at that time
    """
    
    # if data.username:
    #     user = db.exec(select(UserRES).where(UserRES.username == data.username)).first()
    # elif data.email:
    #     user = db.exec(select(UserRES).where(UserRES.email == data.email)).first()
    # else:
    #     raise HTTPException(status_code=400, detail="Either provide Username or Email")
    
    if not user:
        raise HTTPException(status_code=400, detail="User Not Found")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Your Password is not correct")
    
    token = create_access_token(data = user, expires_delta = access_token)
    
    return {"access_token": token, "token_type": "bearer"}


def update_user_first_name(db: DB_SESSION, first_name: str, user_id: int):
    update_user_first_name: User | None = db.get(User, user_id)
    
    if not update_user_first_name:
        raise HTTPException(status_code=400, detail="User Not Found")
    
    if first_name:
        if not strict_first_name(first_name):
            raise HTTPException(status_code=400, detail="Your Updated First Name is not valid")
        update_user_first_name.first_name = first_name
        
    db.add(update_user_first_name)
    db.commit()
    db.refresh(update_user_first_name)
    return {"updated_first_name": f"Your First Name Updated Success Fully  {first_name}"}
    
def update_user_last_name(db: DB_SESSION, last_name: str, user_id: int):
    update_user_last_name: User | None = db.get(User, user_id)
    
    if not update_user_last_name:
        raise HTTPException(status_code=400, detail="User Not Found")
    
    if last_name:
        if not strict_last_name(last_name):
            raise HTTPException(status_code=400, detail="Your Updated Last Name is not valid")
        update_user_last_name.last_name = last_name
    

    
    db.add(update_user_last_name)
    db.commit()
    db.refresh(update_user_last_name)
    return {"updated_last_name": f"Your Last Name Updated Success Fully {last_name}"}

def update_user_username(db: DB_SESSION, username: str, user_id: int):
    update_user_username: User | None = db.get(User, user_id)
    
    if not update_user_username:
        raise HTTPException(status_code=400, detail="User Not Found")
    
    if username:
        if not strict_username_methods(username):
            raise HTTPException(status_code=400, detail="Your Updated Username is not valid")
        update_user_username.username = username
        
    db.add(update_user_username)
    db.commit()
    db.refresh(update_user_username)
    return {"updated_username": f"Your User Name Updated Success Fully {username}"}

def update_user_email(db: DB_SESSION, email: str, user_id: int):
    update_user_email: User | None = db.get(User, user_id)
    
    if not update_user_email:
        raise HTTPException(status_code=400, detail="User Not Found")
    
    if email:
        if not strict_email_methods(email):
            raise HTTPException(status_code=400, detail="Your Updated email is not valid")
        update_user_email.email = email
        
    db.add(update_user_email)
    db.commit()
    db.refresh(update_user_email)
    return {"updated_email": f"Your new Email Updated Success Fully {email}"}
        
def update_user_password(db: DB_SESSION, old_password: str, updated_new_password: str, user_id: int):
    user: User | None = db.get(User, user_id)
    
    if not user:
        raise HTTPException(status_code=400, detail="User Not Found")
    
    if not verify_password(old_password, user.password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    
    if updated_new_password:
        if not strong_password(updated_new_password):
            raise HTTPException(status_code=400, detail="Your new password is not strong enough. Please recreate your password with upper, lower, number, and special characters.")
    
        old_password_hashed = user.password
        hash_new_password = hash_password(updated_new_password)
        user.password = hash_new_password
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"old_password": old_password_hashed, "updated_new_password": f"Your New Password Updated Success Fully {hash_new_password}"}


def update_user_phone_number(db: DB_SESSION, phone_number: str, user_id: int):
    update_user_phone_number: User | None = db.get(User, user_id)
    
    if not update_user_phone_number:
        raise HTTPException(status_code=400, detail="User Not Found")
    
    if phone_number:
        if not phone_number_strict(phone_number):
            raise HTTPException(status_code=400, detail="Please Update Your Phone As Pakistani Number Only")
        update_user_phone_number.phone_number = phone_number
        

    db.add(update_user_phone_number)
    db.commit()
    db.refresh(update_user_phone_number)
    return {"updated_phone_number": f"Your Phone Number Updated Success Fully  {phone_number}"}





def deleted_users(db: DB_SESSION, user_id: int):
    delete_users: User | None = db.get(User, user_id)
    
    if not delete_users:
        raise HTTPException(status_code=400, detail="User Not Found")
    
    db.delete(delete_users)
    db.commit()
    db.close()
    return "User Deleted Success fully"