"""
In-memory database simulation.
Replace this with SQLAlchemy / any real DB in production.
"""
from app.models import User, RoleName

# In-memory stores
_users_db: dict[int, dict] = {}
_next_id: int = 1


def init_db():
    """Seed the database with default users."""
    global _next_id

    defaults = [
        {"username": "superadmin", "email": "superadmin@example.com", "password": "super123", "role": RoleName.SUPER_ADMIN},
        {"username": "admin", "email": "admin@example.com", "password": "admin123", "role": RoleName.ADMIN},
        {"username": "moderator", "email": "mod@example.com", "password": "mod123", "role": RoleName.MODERATOR},
        {"username": "editor", "email": "editor@example.com", "password": "editor123", "role": RoleName.EDITOR},
        {"username": "alice", "email": "alice@example.com", "password": "alice123", "role": RoleName.USER},
        {"username": "guest", "email": "guest@example.com", "password": "guest123", "role": RoleName.GUEST},
    ]

    for u in defaults:
        _users_db[_next_id] = {**u, "id": _next_id, "is_active": True}
        _next_id += 1


def get_all_users() -> list[dict]:
    return list(_users_db.values())


def get_user_by_id(user_id: int) -> dict | None:
    return _users_db.get(user_id)


def get_user_by_username(username: str) -> dict | None:
    for u in _users_db.values():
        if u["username"] == username:
            return u
    return None


def create_user(username: str, email: str, password: str, role: RoleName) -> dict:
    global _next_id
    user = {
        "id": _next_id,
        "username": username,
        "email": email,
        "password": password,
        "role": role,
        "is_active": True,
    }
    _users_db[_next_id] = user
    _next_id += 1
    return user


def update_user_role(user_id: int, new_role: RoleName) -> dict | None:
    user = _users_db.get(user_id)
    if user:
        user["role"] = new_role
    return user


def delete_user(user_id: int) -> bool:
    if user_id in _users_db:
        del _users_db[user_id]
        return True
    return False


def deactivate_user(user_id: int) -> dict | None:
    user = _users_db.get(user_id)
    if user:
        user["is_active"] = False
    return user
