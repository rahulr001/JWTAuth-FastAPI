import hashlib
from jose import jwt
from random import randbytes
from datetime import datetime, timedelta
from utils.database import User
from serializers.AuthSerializer import UserEntity
from fastapi import APIRouter, Request, Depends, HTTPException, status, Response
from schemas.AuthSchema import User_Creation_Schema, User_Login_Schema, Refresh_Token
from utils.jwt_auth import AuthJWT
from utils.config import JWT_ALGORITHM, REFRESH_SECRET_KEY
from bson import ObjectId

router = APIRouter()


@router.post('/register', status_code=status.HTTP_201_CREATED, response_description='user created successfully')
async def register(request: Request, data: User_Creation_Schema):
    user = User.find_one({'email': data.email})
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="a user with same email already exists")
    if data.password != data.password1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='password missmatch')
    data.password = AuthJWT.hash_password(data.password)
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


@router.post('/login', status_code=status.HTTP_202_ACCEPTED, response_description="login successfull")
async def login(data: User_Login_Schema):
    db_user = User.find_one({'email': data.email})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    user = UserEntity(db_user)
    verify_pass = AuthJWT.verify_password(data.password, user['password'])

    if not verify_pass:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    access_token = AuthJWT.generate_access_token(str(user['id']))
    refresh_token = AuthJWT.generate_refresh_token(str(user['id']))
    return {'status': 'success', 'response': {'access_token': access_token, 'refresh_token': refresh_token}}


@router.post('/refresh', status_code=status.HTTP_201_CREATED, response_description='token refreshed')
async def refresh(data: Refresh_Token):
    print(data)
    user_id = jwt.decode(data.refresh_token,
                         key=REFRESH_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    print(timedelta(minutes=10)+datetime.utcnow())
    user = User.find_one({'_id': ObjectId(user_id['sub'])})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Refresh Token Invalid")
    access_token = AuthJWT.generate_access_token(user_id['sub'])
    return {'status': 'success', 'access_token': access_token}


@router.post('test')
async def test(data: Response):
    data.set_cookie('test','test')
    print(dir(data))
