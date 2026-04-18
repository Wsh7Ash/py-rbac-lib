from fastapi import APIRouter, Depends, HTTPException, status
from app.models import UserResponse, UserCreate, Permission, RoleName
from app.auth import require_permission, get_current_user, get_user_permissions
from app.database import get_all_users, get_user_by_id, create_user, get_user_by_username

router = APIRouter()


def _to_response(user: dict) -> UserResponse:
    return UserResponse(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        role=user["role"],
        is_active=user["is_active"],
        permissions=get_user_permissions(user["role"]),
    )


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user=Depends(get_current_user)):
    """Get the current user's profile."""
    user = get_user_by_username(current_user.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _to_response(user)


@router.get("/", response_model=list[UserResponse])
def list_users(_=Depends(require_permission(Permission.READ_USERS))):
    """List all users (requires read:users permission)."""
    return [_to_response(u) for u in get_all_users()]


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, _=Depends(require_permission(Permission.READ_USERS))):
    """Get a specific user by ID (requires read:users permission)."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _to_response(user)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(data: UserCreate, _=Depends(require_permission(Permission.WRITE_USERS))):
    """Create a new user (requires write:users permission)."""
    if get_user_by_username(data.username):
        raise HTTPException(status_code=409, detail="Username already exists")
    user = create_user(data.username, data.email, data.password, data.role or RoleName.USER)
    return _to_response(user)
