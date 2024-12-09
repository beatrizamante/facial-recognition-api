
from typing import Optional
from fastapi import Depends, HTTPException, status
from pytest import Session
from app.db.db_for_endpoints import Usuario
from app.services.auth_services import decode_token
from app.utils.db_get import get_db


def get_current_user(user_id: Optional[str] = Depends(decode_token), db: Session = Depends(get_db)):
    #For testing purposes
    if user_id is None:
        return None 

    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user