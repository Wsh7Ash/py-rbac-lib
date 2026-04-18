"""
Authentication and authorization utilities.
"""
import hashlib
import hmac
import json
import time
from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.models import Permission, RoleName, ROLE_PERMISSIONS, TokenData
from app.database import get_user_by_username

# Simple secret for HMAC-based token signing (use a real JWT library in production)
SECRET_KEY = "change-me-in-production"

security = HTTPBearer()


def _sign(payload: str) -> str:
    return hmac.HMAC(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()


def create_token(username: str, role: RoleName) -> str:
    """Create a simple signed token (use PyJWT in production)."""
    payload = json.dumps({"username": username, "role": role.value, "exp": int(time.time()) + 3600})
    signature = _sign(payload)
    import base64
    token = base64.urlsafe_b64encode(f"{payload}|{signature}".encode()).decode()
    return token


def decode_token(token: str) -> TokenData:
    """Decode and verify a token."""
    import base64
    try:
        decoded = base64.urlsafe_b64decode(token.encode()).decode()
        payload_str, signature = decoded.rsplit("|", 1)
        if not hmac.compare_digest(_sign(payload_str), signature):
            raise ValueError("Invalid signature")
        payload = json.loads(payload_str)
        if payload.get("exp", 0) < time.time():
            raise ValueError("Token expired")
        return TokenData(username=payload["username"], role=RoleName(payload["role"]))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """Extract and validate the current user from the Authorization header."""
    return decode_token(credentials.credentials)


def require_role(*roles: RoleName) -> Callable:
    """Dependency that requires the user to have one of the specified roles."""
    def role_checker(current_user: TokenData = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {[r.value for r in roles]}",
            )
        return current_user
    return role_checker


def require_permission(*permissions: Permission) -> Callable:
    """Dependency that requires the user to have ALL of the specified permissions."""
    def permission_checker(current_user: TokenData = Depends(get_current_user)):
        user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])
        missing = [p.value for p in permissions if p not in user_permissions]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permissions: {missing}",
            )
        return current_user
    return permission_checker


def get_user_permissions(role: RoleName) -> list[str]:
    """Get the list of permission strings for a given role."""
    return [p.value for p in ROLE_PERMISSIONS.get(role, [])]
