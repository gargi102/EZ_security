from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from app import models, database, utils
from app.schema_definitions import UserLogin, TokenOut, UserSignup, UserOut, UserRole
from app.utils import create_access_token




router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_auth():
    return {"message": "auth router working"}


@router.post("/login", response_model=TokenOut)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    
    if not db_user.is_verified:
        raise HTTPException(status_code=401, detail="Please verify your email before login.")

    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    
    token_data = {
        "sub": db_user.email,
        "role": db_user.role.value
    }

    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    email = utils.verify_verification_token(token)
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.is_verified:
        return {"message": "User already verified."}

    user.is_verified = True
    db.commit()
    return {"message": "✅ Email verified successfully."}


@router.post("/signup", response_model=UserOut)
def signup(user: UserSignup, db: Session = Depends(get_db)):
    # Allow only CLIENT users to sign upn
    if user.role != UserRole.CLIENT:
        raise HTTPException(status_code=403, detail="Only client users can sign up.")

    hashed_password = pwd_context.hash(user.password)
    new_user = models.User(
        email=user.email,
        password=hashed_password,
        role=user.role,
        is_verified=False
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered.")

    # Generate verification token
    token = utils.generate_verification_token(user.email)
    verification_link = f"http://localhost:8000/verify-email?token={token}"

    print("🔗 Email verification link:", verification_link)  # Simulate sending email

    return new_user
