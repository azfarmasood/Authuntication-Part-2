from fastapi import HTTPException
from passlib.context import CryptContext
import re
from jose import jwt
from models.user_models import User
from db.settings import secret_key, algorithem
from datetime import timedelta, timezone, datetime

# This will strict First Name and Last Name
def strict_first_name(first_name: str) -> bool:
    pattern = r'^[A-Za-z\s]*$'
    
    if not re.match(pattern, first_name):
        raise HTTPException(status_code=400, detail="First Name should only contain alphabets (A-Z or a-z) and spaces")
    
    return True

def strict_last_name(last_name: str) -> bool:
    pattern = r'^[A-Za-z\s]*$'
    
    if not re.match(pattern, last_name):
        raise HTTPException(status_code=400, detail="Last Name should only contain alphabets (A-Z or a-z) and spaces")
    
    return True


# This will strict username
def strict_username_methods(username: str):
    pattern = r'^[a-zA-Z0-9]+$'
    if not re.match(pattern, username):
        raise HTTPException(status_code=400, detail="Your username is incorrect please use the following patterns (A-Z or a-z 1-9)")
    return True

# This Will Strict Email Domains While Creating Emails
def strict_email_methods(email: str) -> bool:
    pattern = r'^(.+)@(gmail\.com|outlook\.com|yahoo\.com)$'
    if not re.match(pattern, email):
        raise HTTPException(status_code=400, detail="Your domain name is incorrect please use the following email patterns (gmail.com/outlook.com/yahoo.com)")
    return True

def phone_number_strict(phone_number: str) -> bool:
    if len(phone_number) != 11:
        raise HTTPException(status_code=400, detail="Use only pakistani number that used for only 11 digits")
    return True

# This Will ask the user to create strong password
def strong_password(password: str) -> bool:
    SPECIAL_CHARACTER = ['!', '@', '#', '$', '%', '^', '&', '*', '=', ':', '?', '.', '/', '~', '<', '>']
    if len(password) < 8 or len(password) > 20:   
        raise HTTPException(status_code=400, detail="Your Password must be between 8 or 20 characters")
    
    if not any(character.isupper() for character in password) or not any(character.islower() for character in password) or not any(character.isdigit() for character in password) or not any(character in SPECIAL_CHARACTER for character in password):
        raise HTTPException(status_code=400, detail="Your password must be upper, lower, number and special characters")
    
    return True
    
# Convert string password in to hashing password
def hash_password(password: str):
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password: str = pwd_context.hash(password)
    return hashed_password

# This will verify plain password in to hashpassword and converting in to hash digits
def verify_password(plain_password:str, hash_password: str):
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hash = hash_password)


# This Will Create Access Token:

def create_access_token(data: User, expires_delta: timedelta):
    expires_time = datetime.now(timezone.utc) + expires_delta
    expires = int(expires_time.timestamp())
    encode: dict = {
        "name": f"{data.first_name} {data.last_name}",
        "username": data.username,
        "expires": expires
    }
    headers: dict = {
        "kong_id": data.kong_id
    } 
    
    jwt_encode = jwt.encode(encode, key = secret_key, algorithm = algorithem, headers = headers)
    
    return jwt_encode