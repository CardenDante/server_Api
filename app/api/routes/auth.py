# app/api/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.core.security import create_access_token, verify_password, get_password_hash, get_current_user
from datetime import timedelta
from app.core.config import settings
from typing import Dict

router = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# In production, use a database
USERS = {
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash(settings.ADMIN_PASSWORD)  # Get from env
    }
}

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict:
    user = USERS.get(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/create-api-key")
async def create_new_api_key(current_user: str = Depends(get_current_user)) -> Dict:
    if current_user != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    from app.core.security import create_api_key
    new_key = create_api_key()
    
    return {"api_key": new_key}