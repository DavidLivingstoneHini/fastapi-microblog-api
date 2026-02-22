from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User CRUD Operations
def get_user_by_username_or_email(db: Session, username: str, email: str):
    """Get user by username or email"""
    return db.query(models.User).filter(
        (models.User.username == username) | (models.User.email == email)
    ).first()

def get_user_by_login(db: Session, login: str):
    """Get user by username or email for login"""
    return db.query(models.User).filter(
        (models.User.username == login) | (models.User.email == login)
    ).first()

def get_user_by_id(db: Session, user_id: int):
    """Get user by ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Create new user with hashed password"""
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

# Post CRUD Operations
def get_posts(db: Session, skip: int = 0, limit: int = 10):
    """Get paginated posts, newest first"""
    return db.query(models.Post).order_by(
        models.Post.created_at.desc()
    ).offset(skip).limit(limit).all()

def get_post_count(db: Session):
    """Get total number of posts"""
    return db.query(func.count(models.Post.id)).scalar()

def get_post_by_id(db: Session, post_id: int):
    """Get post by ID"""
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_user_posts(db: Session, user_id: int):
    """Get all posts by a specific user"""
    return db.query(models.Post).filter(
        models.Post.author_id == user_id
    ).order_by(models.Post.created_at.desc()).all()

def create_post(db: Session, post: schemas.PostCreate, author_id: int):
    """Create new post"""
    db_post = models.Post(
        title=post.title,
        content=post.content,
        author_id=author_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
