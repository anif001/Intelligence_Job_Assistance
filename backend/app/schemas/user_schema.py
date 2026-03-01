from pydantic import BaseModel, EmailStr, Field, Field
from typing import Optional
class UserRegistration(BaseModel):
   name: str
   email: EmailStr
   password: str=Field(..., min_length=6,max_length=72)
   college_tier: Optional[int] = None