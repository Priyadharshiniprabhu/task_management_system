from fastapi import Depends
from fastapi import HTTPException, status

from app.auth import get_current_user

def admin_required(current_user=Depends(get_current_user)):

    if current_user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can access")
    return current_user