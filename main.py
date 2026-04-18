from fastapi import FastAPI
from app.routes import auth, users, admin
from app.database import init_db

app = FastAPI(
    title="py-rbac-lib",
    description="A Python RBAC (Role-Based Access Control) library and API template",
    version="1.0.0",
)

# Initialize in-memory database with default data
init_db()

# Register route modules
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])


@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to py-rbac-lib!",
        "docs": "/docs",
        "version": "1.0.0",
    }
