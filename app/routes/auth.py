from fastapi import APIRouter, HTTPException, status
from app.models import LoginRequest, TokenResponse
from app.database import get_user_by_username
from app.auth import create_token, get_user_permissions

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    """Authenticate a user and return an access token."""
    user = get_user_by_username(request.username)
    if not user or user["password"] != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    token = create_token(user["username"], user["role"])
    permissions = get_user_permissions(user["role"])

    return TokenResponse(
        access_token=token,
        role=user["role"].value,
        permissions=permissions,
    )


@router.get("/roles")
def list_roles():
    """List all available roles and their permissions."""
    from app.models import ROLE_PERMISSIONS
    return {
        role.value: [p.value for p in perms]
        for role, perms in ROLE_PERMISSIONS.items()
    }
