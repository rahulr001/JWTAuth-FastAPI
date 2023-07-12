import hashlib
from random import randbytes
from datetime import datetime
from utils.database import User
from serializers.AuthSerializer import UserEntity
from utils.auth_config import hash_password, verify_password
from fastapi import APIRouter, Request, Depends, HTTPException, status
from schemas.AuthSchema import User_Creation_Schema, User_Login_Schema

router = APIRouter()


@router.post('/register')
async def register(request: Request, data: User_Creation_Schema):
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
    try:
        token = randbytes(10)
        hash = hashlib.sha256()
        hash.update(token)
        verification_code = hash.hexdigest()
        user = User.find_one_and_update({'_id': result.inserted_id}, {
                                        '$set': {'verification_code': verification_code, 'updated_at': datetime.utcnow()}})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='could not generate verification code')
    return {'status': 'success', 'response': "user created successfully"}


@router.post('/login', response_description="login successfull")
async def login(data: User_Login_Schema):
    db_user = User.find_one({'email': data.email})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    user = UserEntity(db_user)
    verify_pass = verify_password(data.password, user['password'])

    if not verify_pass:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    return {'status': 'success'}
