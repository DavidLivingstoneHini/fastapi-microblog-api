from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])
security = HTTPBasic()


def get_current_user(
        credentials: HTTPBasicCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    """Authenticate and return current user (dependency for protected routes)"""
    user = crud.get_user_by_login(db, credentials.username)

    if not user or not crud.verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user


@router.post("", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
        post: schemas.PostCreate,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Create a new blog post

    Requires Basic Authentication

    - **title**: Post title (1-200 characters)
    - **content**: Post content (minimum 1 character)
    """
    return crud.create_post(db, post, current_user.id)


@router.get("", response_model=schemas.PaginatedPosts)
def list_posts(
        page: int = 1,
        page_size: int = 10,
        db: Session = Depends(get_db)
):
    """
    List all posts with pagination

    - **page**: Page number (default: 1, minimum: 1)
    - **page_size**: Items per page (default: 10, min: 1, max: 50)
    """
    # Validate pagination parameters
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page must be greater than or equal to 1"
        )

    if page_size < 1 or page_size > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page size must be between 1 and 50"
        )

    # Calculate offset
    skip = (page - 1) * page_size

    # Get paginated posts and total count
    posts = crud.get_posts(db, skip=skip, limit=page_size)
    total = crud.get_post_count(db)
    pages = (total + page_size - 1) // page_size if total > 0 else 1

    return {
        "items": posts,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages
    }


@router.get("/{post_id}", response_model=schemas.PostWithAuthor)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    Get a specific post by ID with author details

    - **post_id**: ID of the post to retrieve
    """
    post = crud.get_post_by_id(db, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )

    return post
