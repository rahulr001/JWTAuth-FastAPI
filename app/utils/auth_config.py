from passlib.context import CryptContext

context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return context.hash(password)


def verify_password(password: str, hashed_password: str) -> str:
    return context.verify(password, hashed_password)
