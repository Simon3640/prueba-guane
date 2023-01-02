from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Bcrypt:

    def get_password_hash(plain_password: str) -> str:
        return pwd_context.hash(plain_password)
    
    def check_password(plain_password: str, hashed_password:str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


bcrypt = Bcrypt()