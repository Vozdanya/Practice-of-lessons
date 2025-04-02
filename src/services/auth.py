from datetime import timezone, datetime, timedelta

from fastapi import HTTPException, status
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from src.config import settings


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str: # Создание jwt-токена
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def hash_password(self, password: str) -> str: # Хеширование пароля
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool: # Проверка совпадения пароля при аутентификации
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate(self, base_password, user_password):
        # Проверка на существование пользователя и на совпадение введенного пароля
        if user_password and authservice.verify_password(base_password, user_password):
            return True

    def decode_token(self, token):
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def replacement_with_hashed_password(self, data: BaseModel, schema) -> BaseModel:
        user_data_dict = data.model_dump(exclude={"password"}, exclude_unset=True)
        return schema(**user_data_dict, hashed_password=self.pwd_context.hash(data.password))


authservice = AuthService()