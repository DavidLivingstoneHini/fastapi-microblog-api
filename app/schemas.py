import re
from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr, Field, field_validator


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """Username must be alphanumeric"""
        if not v.isalnum():
            raise ValueError('Username must contain only letters and numbers')
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Password validation"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if len(v) > 100:
            raise ValueError('Password cannot exceed 100 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
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

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v):
        """Ensure title is not just whitespace"""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

    @field_validator('content')
    @classmethod
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
