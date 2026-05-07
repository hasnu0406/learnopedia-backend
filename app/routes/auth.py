from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.auth_service import create_user, authenticate_user, create_access_token

router = APIRouter()

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(data: SignupRequest):
    user_id, error = create_user(data.email, data.password, data.name)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "Account created successfully", "user_id": user_id}

@router.post("/login")
def login(data: LoginRequest):
    user = authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}