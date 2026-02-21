from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

    @validator('username')
    def validate_username(cls, v):
        """Username must be alphanumeric"""
        if not v.isalnum():
            raise ValueError('Username must contain only letters and numbers')
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

    @validator('password')
    def validate_password(cls, v):
        """Basic password strength validation"""
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Post Schemas
class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)

    @validator('title')
    def title_not_empty(cls, v):
        """Ensure title is not just whitespace"""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

    @validator('content')
    def content_not_empty(cls, v):
        """Ensure content is not just whitespace"""
        if not v or not v.strip():
            raise ValueError('Content cannot be empty')
        return v.strip()


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PostWithAuthor(PostResponse):
    author: UserResponse

    class Config:
        from_attributes = True


# Pagination
class PaginatedPosts(BaseModel):
    items: List[PostResponse]
    total: int
    page: int
    page_size: int
    pages: int

    class Config:
        from_attributes = True
