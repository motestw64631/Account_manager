from sqlalchemy.orm import Session

from app.user import models, schemas
from passlib.hash import pbkdf2_sha256

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pbkdf2_sha256.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_user(db: Session, user:schemas.UserVerify):
    target_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not target_user:
        return {"success":False, "reason":"User does not exist."}
    if pbkdf2_sha256.verify(user.password, target_user.hashed_password):
        return {"success":True}  
    else:
        return {"success":False, "reason":"Invalid password."} 