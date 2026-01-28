from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from database.database import get_db
from schemas.auth import UserCreate, UserLogin, UserResponse, Token, UserUpdate
from services.auth_service import AuthService
from utils.security import create_access_token, verify_password, get_password_hash
from api.middlewares.auth_middleware import JWTBearer, get_current_user
from config.settings import settings

router = APIRouter(tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# وابستگی برای سرویس احراز هویت
def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)

@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate, 
    auth_service: AuthService = Depends(get_auth_service)
):
    """ثبت‌نام کاربر جدید"""
    try:
        user = auth_service.register_user(user_data)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در ثبت‌نام: {str(e)}"
        )

@router.post("/auth/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """ورود کاربر و دریافت توکن"""
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="نام کاربری یا رمز عبور اشتباه است",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="حساب کاربری غیرفعال است"
        )
    
    # ایجاد توکن دسترسی
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username, 
            "user_id": user.id,
            "email": user.email,
            "is_admin": user.is_admin
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # ثانیه
    }

@router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """دریافت اطلاعات کاربر جاری"""
    user = auth_service.get_user_by_id(current_user["user_id"])
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="کاربر یافت نشد"
        )
    
    return user

@router.put("/auth/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """بروزرسانی اطلاعات کاربر جاری"""
    user = auth_service.update_user(current_user["user_id"], user_update)
    return user

@router.post("/auth/change-password")
async def change_password(
    old_password: str,
    new_password: str,
    current_user: dict = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """تغییر رمز عبور"""
    success = auth_service.change_password(
        current_user["user_id"], 
        old_password, 
        new_password
    )
    
    if success:
        return {"message": "رمز عبور با موفقیت تغییر کرد"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="رمز عبور قدیمی اشتباه است"
        )

@router.post("/auth/logout")
async def logout():
    """خروج کاربر (در سمت کلاینت توکن حذف شود)"""
    return {"message": "با موفقیت خارج شدید"}

@router.get("/auth/check-username/{username}")
async def check_username_availability(
    username: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    """بررسی در دسترس بودن نام کاربری"""
    exists = auth_service.check_username_exists(username)
    return {"available": not exists, "username": username}

@router.get("/auth/check-email/{email}")
async def check_email_availability(
    email: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    """بررسی در دسترس بودن ایمیل"""
    exists = auth_service.check_email_exists(email)
    return {"available": not exists, "email": email}

# فقط برای ادمین‌ها
@router.get("/auth/users", dependencies=[Depends(JWTBearer())])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    auth_service: AuthService = Depends(get_auth_service),
    current_user: dict = Depends(get_current_user)
):
    """دریافت لیست تمام کاربران (فقط ادمین)"""
    # بررسی ادمین بودن
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="دسترسی ادمین لازم است"
        )
    
    users = auth_service.get_all_users(skip, limit)
    return users