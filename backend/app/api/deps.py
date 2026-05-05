from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.staff import Staff
from app.services.auth_service import get_staff_by_id


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_staff(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Staff:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보가 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
    except ValueError:
        raise credentials_error

    sub = payload.get("sub")
    organization_id = payload.get("organization_id")
    if sub is None or organization_id is None:
        raise credentials_error

    try:
        staff_id = int(sub)
    except (TypeError, ValueError):
        raise credentials_error

    staff = get_staff_by_id(db, staff_id)
    if staff is None:
        raise credentials_error

    if staff.organization_id != organization_id:
        raise credentials_error

    return staff
