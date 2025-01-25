# app/api/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, verify_password, get_password_hash, get_current_user
from datetime import timedelta
from app.core.config import settings
from typing import Dict

router = APIRouter(prefix="/auth", tags=["authentication"])

# In production, use a database
USERS = {
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash("admin123")  # Change this!
    }
}

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict:
    user = USERS.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
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
            detail="Not authorized to create API keys"
        )
    
    from app.core.security import create_api_key
    new_key = create_api_key()
    
    # In production, store this securely
    return {"api_key": new_key}