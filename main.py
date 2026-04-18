from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Python RBAC Lib")

# Mock User DB
class User(BaseModel):
    username: str
    role: str

def get_current_user() -> User:
    # In a real application, extract the user from a JWT token
    return User(username="alice", role="admin")

def require_role(required_role: str):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires role: {required_role}"
            )
        return user
    return role_checker

@app.get("/")
def read_root():
    return {"message": "Welcome to Python RBAC Lib!"}

@app.get("/admin-only", dependencies=[Depends(require_role("admin"))])
def admin_route():
    return {"message": "This is a restricted admin route!"}
