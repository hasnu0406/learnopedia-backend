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
    try:
        user_id, error = create_user(data.email, data.password, data.name)
        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"message": "Account created successfully", "user_id": user_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.post("/login")
def login(data: LoginRequest):
    try:
        user = authenticate_user(data.email, data.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        token = create_access_token({"sub": user["email"]})
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")