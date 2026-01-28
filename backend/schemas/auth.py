from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List
from datetime import datetime
import re

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="نام کاربری")
    email: EmailStr = Field(..., description="آدرس ایمیل")
    full_name: Optional[str] = Field(None, max_length=100, description="نام کامل")
    phone_number: Optional[str] = Field(None, pattern=r'^09\d{9}$', description="شماره موبایل ایرانی")

    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('نام کاربری فقط می‌تواند شامل حروف انگلیسی، اعداد و زیرخط باشد')
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100, description="رمز عبور")
    confirm_password: str = Field(..., description="تکرار رمز عبور")

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('رمز عبور و تکرار آن مطابقت ندارند')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('رمز عبور باید حداقل ۶ کاراکتر باشد')
        # می‌توانید قوانین بیشتری اضافه کنید
        return v

class UserLogin(BaseModel):
    username: str = Field(..., description="نام کاربری یا ایمیل")
    password: str = Field(..., description="رمز عبور")

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    expires_in: int = 1800  # 30 دقیقه به ثانیه

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

class PasswordChange(BaseModel):
    old_password: str
    new_password: str
    confirm_new_password: str

    @validator('confirm_new_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('رمز عبور جدید و تکرار آن مطابقت ندارند')
        return v