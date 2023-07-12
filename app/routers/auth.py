from fastapi import APIRouter, Request, Depends, HTTPException, status
from schemas.AuthSchema import User_Creation
from utils.database import User
from utils.auth_config import hash_password
from datetime import datetime

router = APIRouter()


@router.post('/register')
async def register(request: Request, data: User_Creation):
    user = User.find_one({'email': data.email})
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="a user with same email already exists")
    if data.password != data.password1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='passwor missmatch')
    data.password = hash_password(data.password)
    del data.password1
    data.created_at = data.updated_at = datetime.utcnow()
    result = User.insert_one(data.dict())
    new_user = User.find_one({'_id': result.inserted_id})
    return {'response': str(result.inserted_id)}
