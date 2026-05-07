from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List
from app.services.groq_service import get_recommendations
from jose import JWTError, jwt
import os

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.getenv("SECRET_KEY", "learnopedia-secret-key-2024")
ALGORITHM  = "HS256"

class RecommendRequest(BaseModel):
    interests: List[str]
    skills:    List[str]
    goals:     List[str]

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email   = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/recommend")
def recommend(data: RecommendRequest, current_user: str = Depends(get_current_user)):
    try:
        result = get_recommendations(data.interests, data.skills, data.goals)
        return {"recommendation": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))