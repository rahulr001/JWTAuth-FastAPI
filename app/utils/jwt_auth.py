from jose import jwt
from typing import Union, Any
from datetime import timedelta, datetime
from .config import SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRES_IN, REFRESH_TOKEN_EXPIRES_IN, REFRESH_SECRET_KEY


class AuthJWT:
    def generate_access_token(subject: Union[str, Any], exp_date: Union[int, None] = None):
        if exp_date:
            expiration_date = datetime.utcnow()+exp_date
        else:
            expiration_date = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)

        token_data = {'exp': expiration_date, 'sub': subject}
        return jwt.encode(token_data, algorithm=JWT_ALGORITHM, key=SECRET_KEY)

    def generate_refresh_token(subject: Union[str, Any], exp_date: Union[int, None] = None):
        if exp_date:
            expiration_date = datetime.utcnow()+exp_date
        else:
            expiration_date = datetime.utcnow()+timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN)

        token_data = {'exp': expiration_date, 'sub': subject}
        return jwt.encode(token_data, algorithm=JWT_ALGORITHM, key=REFRESH_SECRET_KEY)
