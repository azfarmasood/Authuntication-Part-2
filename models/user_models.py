from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
import uuid

# Create Users Base Start: 
# ======================================================

class UserBase(SQLModel):
    id: Optional[int] = Field(default = None, primary_key = True)

# Create Users Base End:
# ======================================================



# Create Users Res Body Start:
# ======================================================

class User(UserBase, table=True):
    first_name: str = Field(default = str, regex = r'^[A-Za-z\s]*$', max_length = 20, index=True)
    last_name: str = Field(default = str, regex = r'^[A-Za-z\s]*$', max_length = 20, index=True)
    username: str = Field(default = str, regex = r'^[A-Za-z0-9]*$', max_length = 30, unique=True)
    email: str = Field(default = str, regex = r'^(.+)@(gmail\.com|outlook\.com|yahoo\.com)$', max_length = 50, unique=True)
    password: str = Field(default = str, max_length = 100)
    phone_number: str = Field(default = str, regex = r'^\+92\d{10}$', max_length = 11)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_verified: bool = Field(default = True)
    kong_id: str = Field(default_factory = lambda: uuid.uuid4().hex)

# Create Users Res Body End:
# ======================================================



# Create Users Req Body Start:
# ======================================================

class UserREQ(SQLModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    phone_number: str
    

    
# Update Models Which Can User Update Base Upon Their Requests
# ==============================================================
# ==============================================================

class UserUpdateFirstName(SQLModel):
    updated_first_name: str
    
class UserUpdateLastName(SQLModel):
    updated_last_name: str
    
class UserUpdateUsername(SQLModel):
    updated_username: str
    
class UserUpdateEmail(SQLModel):
    updated_email: str
    
class UserUpdatePassword(SQLModel):
    old_password: str
    updated_new_password: str

class UserUpdatePhoneNumber(SQLModel):
    updated_phone_number: str

# ==============================================================
# ==============================================================
# Create Users Req Body End:
# ======================================================


# Request Login Start:
# ======================================================

class LoginREQ(SQLModel):
    username: str | None
    password: str
    
# Request Login END:
# ======================================================

# Token Model Start
# ======================================================

class TokenRES(SQLModel):
    access_token: str
    token_type: str
    
# Request Login END:
# ======================================================