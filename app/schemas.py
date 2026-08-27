from pydantic import BaseModel
from pydantic import EmailStr

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    role: str