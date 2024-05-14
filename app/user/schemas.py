from pydantic import BaseModel, field_validator, Field
from typing import Annotated
from pydantic import BaseModel, StringConstraints
import re

class UserBase(BaseModel):
    username: str = Field(description="a string representing the desired username for the account,\
                           with a minimum length \of 3 characters and a maximum length of 32 characters."
                          , min_length=3 , max_length=32)

class UserCreate(UserBase):
    password: str = Field(description="a string representing the desired password for the account,\
                           with aminimum length of 8 characters and a maximum length of 32 characters,\
                          containing at least 1 uppercase letter, 1 lowercase letter, and 1 number.", 
                          min_length=8 , max_length=32)

    @field_validator('password')
    def password_constraints(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        return v
    
class UserVerify(BaseModel):
    username: str = Field(description="a string representing the username of the account being accessed.")
    password: str = Field(description="a string representing the password being used to access the account.")


class ResponseModel(BaseModel):
    success: bool = True

class ErrorResponse(BaseModel):
    success: bool = False
    reason: str 