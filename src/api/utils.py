from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

""" password hashing function"""


def hash(password: str):
    return pwd_context.hash(password)


""" check password"""


def varify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
