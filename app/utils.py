from itsdangerous import URLSafeTimedSerializer
from fastapi import HTTPException
import os
from jose import jwt
from datetime import datetime, timedelta

print("✅ utils.py loaded")

SECRET_KEY = os.environ.get("SECRET_KEY", "my-super-secret-key")  # Replace in prod

serializer = URLSafeTimedSerializer(SECRET_KEY)

JWT_SECRET = "your_jwt_secret_key"  # Replace with env var in real app
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 30

# Create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=JWT_EXPIRATION_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


# Generate a signed email token
def generate_verification_token(email: str):
    return serializer.dumps(email, salt="email-verify")

# Decode a signed email token
def verify_verification_token(token: str, expiration=3600):
    try:
        email = serializer.loads(token, salt="email-verify", max_age=expiration)
        return email
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")
