from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user: User) -> User:
        """ایجاد کاربر جدید"""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """دریافت کاربر با ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """دریافت کاربر با نام کاربری"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """دریافت کاربر با ایمیل"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_username_or_email(self, username_or_email: str) -> Optional[User]:
        """دریافت کاربر با نام کاربری یا ایمیل"""
        return self.db.query(User).filter(
            or_(
                User.username == username_or_email,
                User.email == username_or_email
            )
        ).first()
    
    def update(self, user: User) -> User:
        """بروزرسانی کاربر"""
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        """حذف کاربر"""
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """دریافت لیست تمام کاربران"""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """دریافت لیست کاربران فعال"""
        return self.db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    
    def search_users(self, search_term: str, skip: int = 0, limit: int = 100) -> List[User]:
        """جستجوی کاربران"""
        return self.db.query(User).filter(
            or_(
                User.username.ilike(f"%{search_term}%"),
                User.email.ilike(f"%{search_term}%"),
                User.full_name.ilike(f"%{search_term}%")
            )
        ).offset(skip).limit(limit).all() 
