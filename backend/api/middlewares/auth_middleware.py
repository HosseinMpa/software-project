from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from utils.security import verify_token, get_current_user_from_token

class JWTBearer(HTTPBearer):
    """Middleware برای احراز هویت با JWT"""
    
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        credentials = await super(JWTBearer, self).__call__(request)
        
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="طرح احراز هویت اشتباه است"
                )
            
            # اعتبارسنجی توکن
            payload = verify_token(credentials.credentials)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="توکن نامعتبر یا منقضی شده است"
                )
            
            # ذخیره اطلاعات کاربر در request state
            request.state.user = payload
            
            return credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="اعتبارسنجی لازم است"
            )

# Dependency برای دریافت کاربر جاری
def get_current_user(request: Request):
    """دریافت کاربر جاری از request"""
    if not hasattr(request.state, "user"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="کاربر احراز هویت نشده است"
        )
    return request.state.user

# Dependency برای بررسی ادمین بودن
def get_current_admin_user(request: Request):
    """دریافت کاربر ادمین"""
    user = get_current_user(request)
    
    # اینجا باید بررسی کنیم که کاربر ادمین هست یا نه
    # فعلاً برای سادگی، یک فیلد is_admin در توکن اضافه می‌کنیم
    if not user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="دسترسی ادمین لازم است"
        )
    
    return user