from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas.user import UserCreate, UserLogin
from app.db.crud import CRUDUser

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(deps.get_db)):
    db_user = CRUDUser.get_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    
    db_user = CRUDUser.create(
        db=db,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    
    return {"message": "User created successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(deps.get_db)):
    db_user = CRUDUser.get_by_email(db, user.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
