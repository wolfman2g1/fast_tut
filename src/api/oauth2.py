from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from src.api import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
"""Secret"""
SECRET_KEY = "hvgECHEbgDBF889TXxh5srgSZouGEmmZhYGAufQefSZCSAVmZED7cwfpFd9HuEhb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

"""Create access token"""


def create_access_token(data: dict):
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiration})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError as e:
        print(e)
        raise credentials_exception
    except AssertionError as e:
        print(e)
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credencials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"could not valid credentials", headers={"WWW_AUTHENTICATE": "BEARER"})
    return verify_access_token(token, credencials_exception)
