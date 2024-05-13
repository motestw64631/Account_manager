from pydantic import BaseModel, field_validator
from typing import Annotated
from pydantic import BaseModel, StringConstraints
import re

class UserBase(BaseModel):
    username: Annotated[str, StringConstraints(min_length=3, max_length=32)]


class UserCreate(UserBase):
    password: Annotated[str, StringConstraints(min_length=8, max_length=32)]

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
    username: str
    password: str