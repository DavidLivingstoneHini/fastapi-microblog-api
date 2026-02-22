from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])
security = HTTPBasic()


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user

    - **email**: Valid email address (must be unique)
    - **username**: Alphanumeric, 3-50 characters (must be unique)
    - **password**: At least 6 characters
    """
    # Check if user already exists
    existing_user = crud.get_user_by_username_or_email(db, user.username, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )

    # Create new user
    return crud.create_user(db, user)


@router.get("/me", response_model=schemas.UserResponse)
def get_current_user(
        credentials: HTTPBasicCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    """
    Get currently authenticated user information
    """
    # Find user by username or email
    user = crud.get_user_by_login(db, credentials.username)

    # Verify credentials
    if not user or not crud.verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user


@router.get("/{user_id}/posts", response_model=list[schemas.PostResponse])
def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    """
    Get all posts by a specific user

    - **user_id**: ID of the user
    """
    # Check if user exists
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    # Get user's posts
    return crud.get_user_posts(db, user_id)
