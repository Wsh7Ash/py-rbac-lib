from fastapi import APIRouter, Depends, HTTPException
from app.models import Permission, RoleName, UserResponse, ROLE_PERMISSIONS
from app.auth import require_role, require_permission, get_user_permissions
from app.database import (
    get_all_users, get_user_by_id,
    update_user_role, delete_user, deactivate_user,
)

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


@router.get("/dashboard", dependencies=[Depends(require_permission(Permission.VIEW_ADMIN_PANEL))])
def admin_dashboard():
    """Admin dashboard overview (requires view:admin_panel permission)."""
    users = get_all_users()
    total = len(users)
    active = sum(1 for u in users if u["is_active"])
    by_role = {}
    for u in users:
        role = u["role"].value if hasattr(u["role"], "value") else u["role"]
        by_role[role] = by_role.get(role, 0) + 1

    return {
        "total_users": total,
        "active_users": active,
        "inactive_users": total - active,
        "users_by_role": by_role,
    }


@router.put("/users/{user_id}/role")
def change_user_role(
    user_id: int,
    new_role: RoleName,
    _=Depends(require_permission(Permission.MANAGE_ROLES)),
):
    """Change a user's role (requires manage:roles permission)."""
    user = update_user_role(user_id, new_role)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _to_response(user)


@router.delete("/users/{user_id}")
def remove_user(user_id: int, _=Depends(require_permission(Permission.DELETE_USERS))):
    """Permanently delete a user (requires delete:users permission)."""
    if not delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}


@router.put("/users/{user_id}/deactivate")
def deactivate(user_id: int, _=Depends(require_permission(Permission.DELETE_USERS))):
    """Deactivate a user account (requires delete:users permission)."""
    user = deactivate_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _to_response(user)


@router.get("/permissions")
def list_all_permissions(_=Depends(require_role(RoleName.SUPER_ADMIN))):
    """List all permissions grouped by role (super_admin only)."""
    return {
        role.value: [p.value for p in perms]
        for role, perms in ROLE_PERMISSIONS.items()
    }
