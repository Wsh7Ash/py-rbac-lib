# py-rbac-lib

A comprehensive Python RBAC (Role-Based Access Control) template built with FastAPI.

## Features

- **6 predefined roles**: Super Admin, Admin, Moderator, Editor, User, Guest
- **9 granular permissions**: `read:users`, `write:users`, `delete:users`, `read:posts`, `write:posts`, `delete:posts`, `manage:roles`, `view:admin_panel`, `manage:settings`
- **Role-permission mapping**: Each role has a curated set of permissions
- **Token-based authentication**: HMAC-signed tokens (swap for JWT in production)
- **Permission-guarded routes**: Protect endpoints by role or specific permissions
- **Admin dashboard**: User statistics and role management
- **In-memory database**: Easy to swap for SQLAlchemy / PostgreSQL

## Project Structure

```
py-rbac-lib/
├── main.py              # FastAPI app entrypoint
├── requirements.txt
├── README.md
└── app/
    ├── __init__.py
    ├── models.py        # Pydantic models, enums, role-permission map
    ├── database.py      # In-memory DB with CRUD operations
    ├── auth.py          # Token creation, validation, role/permission guards
    └── routes/
        ├── __init__.py
        ├── auth.py      # POST /auth/login, GET /auth/roles
        ├── users.py     # GET/POST /users, GET /users/me
        └── admin.py     # Dashboard, role changes, user deletion
```

## Quick Start

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then visit `http://localhost:8000/docs` for the interactive API documentation.

## Default Users

| Username    | Password   | Role        |
|-------------|------------|-------------|
| superadmin  | super123   | super_admin |
| admin       | admin123   | admin       |
| moderator   | mod123     | moderator   |
| editor      | editor123  | editor      |
| alice       | alice123   | user        |
| guest       | guest123   | guest       |

## API Endpoints

| Method | Endpoint                       | Permission Required     |
|--------|--------------------------------|------------------------|
| POST   | `/auth/login`                  | None                   |
| GET    | `/auth/roles`                  | None                   |
| GET    | `/users/me`                    | Authenticated          |
| GET    | `/users/`                      | `read:users`           |
| GET    | `/users/{id}`                  | `read:users`           |
| POST   | `/users/`                      | `write:users`          |
| GET    | `/admin/dashboard`             | `view:admin_panel`     |
| PUT    | `/admin/users/{id}/role`       | `manage:roles`         |
| DELETE | `/admin/users/{id}`            | `delete:users`         |
| PUT    | `/admin/users/{id}/deactivate` | `delete:users`         |
| GET    | `/admin/permissions`           | `super_admin` role     |
