from pydantic import BaseModel
from enum import Enum
from typing import Optional


class Permission(str, Enum):
    """All available permissions in the system."""
    READ_USERS = "read:users"
    WRITE_USERS = "write:users"
    DELETE_USERS = "delete:users"
    READ_POSTS = "read:posts"
    WRITE_POSTS = "write:posts"
    DELETE_POSTS = "delete:posts"
    MANAGE_ROLES = "manage:roles"
    VIEW_ADMIN_PANEL = "view:admin_panel"
    MANAGE_SETTINGS = "manage:settings"


class RoleName(str, Enum):
    """Predefined roles."""
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    MODERATOR = "moderator"
    EDITOR = "editor"
    USER = "user"
    GUEST = "guest"


# Role -> Permissions mapping
ROLE_PERMISSIONS: dict[RoleName, list[Permission]] = {
    RoleName.SUPER_ADMIN: list(Permission),  # all permissions
    RoleName.ADMIN: [
        Permission.READ_USERS, Permission.WRITE_USERS, Permission.DELETE_USERS,
        Permission.READ_POSTS, Permission.WRITE_POSTS, Permission.DELETE_POSTS,
        Permission.VIEW_ADMIN_PANEL,
    ],
    RoleName.MODERATOR: [
        Permission.READ_USERS,
        Permission.READ_POSTS, Permission.WRITE_POSTS, Permission.DELETE_POSTS,
    ],
    RoleName.EDITOR: [
        Permission.READ_POSTS, Permission.WRITE_POSTS,
    ],
    RoleName.USER: [
        Permission.READ_POSTS,
    ],
    RoleName.GUEST: [],
}


class User(BaseModel):
    """User model."""
    id: int
    username: str
    email: str
    role: RoleName
    is_active: bool = True


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    username: str
    email: str
    password: str
    role: Optional[RoleName] = RoleName.USER


class UserResponse(BaseModel):
    """Schema for user responses (no password)."""
    id: int
    username: str
    email: str
    role: RoleName
    is_active: bool
    permissions: list[str]


class TokenData(BaseModel):
    """JWT token payload data."""
    username: str
    role: RoleName


class LoginRequest(BaseModel):
    """Schema for login requests."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Schema for token responses."""
    access_token: str
    token_type: str = "bearer"
    role: str
    permissions: list[str]
