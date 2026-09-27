import os
from datetime import datetime, timedelta, timezone


from jose import jwt
from dotenv import load_dotenv


load_dotenv()


JWT_SECRET= os.getenv(
    "JWT_SECRET",
    "development-only-secret-change-this"
)

JWT_ALGORITHM= "HS256"
JWT_EXPIRE_MINUTES= 60

def create_access_token(username:str, role:str)-> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=JWT_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "role":role,
        "exp": expire
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM]
    )