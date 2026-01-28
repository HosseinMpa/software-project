from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime

from models.user import User
from schemas.auth import UserCreate, UserUpdate, PasswordChange
from utils.security import get_password_hash, verify_password
from repositories.user_repository import UserRepository

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def register_user(self, user_data: UserCreate) -> User:
        """ثبت‌نام کاربر جدید"""
        # بررسی وجود کاربر
        if self.user_repo.get_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="نام کاربری قبلاً استفاده شده است"
            )
        
        if self.user_repo.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ایمیل قبلاً استفاده شده است"
            )
        
        # ایجاد کاربر جدید
        hashed_password = get_password_hash(user_data.password)
        
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            phone_number=user_data.phone_number,
            hashed_password=hashed_password,
            is_active=True,
            is_admin=False  # به طور پیش‌فرض کاربر عادی
        )
        
        return self.user_repo.create(db_user)
    
    def authenticate_user(self, username_or_email: str, password: str) -> Optional[User]:
        """احراز هویت کاربر با نام کاربری یا ایمیل"""
        # ابتدا با نام کاربری بررسی می‌کنیم
        user = self.user_repo.get_by_username(username_or_email)
        
        # اگر پیدا نشد، با ایمیل بررسی می‌کنیم
        if not user:
            user = self.user_repo.get_by_email(username_or_email)
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """یافتن کاربر با ID"""
        return self.user_repo.get_by_id(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """یافتن کاربر با نام کاربری"""
        return self.user_repo.get_by_username(username)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """یافتن کاربر با ایمیل"""
        return self.user_repo.get_by_email(email)
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        """بروزرسانی اطلاعات کاربر"""
        user = self.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="کاربر یافت نشد"
            )
        
        # بروزرسانی فیلدها
        update_data = user_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if value is not None:
                setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        
        return self.user_repo.update(user)
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """تغییر رمز عبور کاربر"""
        user = self.get_user_by_id(user_id)
        
        if not user:
            return False
        
        if not verify_password(old_password, user.hashed_password):
            return False
        
        user.hashed_password = get_password_hash(new_password)
        user.updated_at = datetime.utcnow()
        
        self.user_repo.update(user)
        return True
    
    def deactivate_user(self, user_id: int) -> bool:
        """غیرفعال کردن حساب کاربری"""
        user = self.get_user_by_id(user_id)
        
        if not user:
            return False
        
        user.is_active = False
        user.updated_at = datetime.utcnow()
        
        self.user_repo.update(user)
        return True
    
    def check_username_exists(self, username: str) -> bool:
        """بررسی وجود نام کاربری"""
        return self.user_repo.get_by_username(username) is not None
    
    def check_email_exists(self, email: str) -> bool:
        """بررسی وجود ایمیل"""
        return self.user_repo.get_by_email(email) is not None
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """دریافت لیست تمام کاربران"""
        return self.user_repo.get_all(skip, limit)