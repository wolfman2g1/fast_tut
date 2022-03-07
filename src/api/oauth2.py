from jose import JOSEError, jwt
from datetime import datetime, timedelta

"""Secret"""
SECRET_KEY  = "hvgECHEbgDBF889TXxh5srgSZouGEmmZhYGAufQefSZCSAVmZED7cwfpFd9HuEhb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expiration = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiration})
    token =jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return token