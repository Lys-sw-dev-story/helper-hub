from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff
from app.core.database import get_db
from app.core.security import create_access_token
from app.models.staff import Staff
from app.schemas.auth_schema import LoginRequest, StaffMe, TokenResponse
from app.services.auth_service import authenticate_staff


router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    staff = authenticate_staff(db, payload.email, payload.password)
    if staff is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
        )

    if staff.organization_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="소속 기관이 지정되지 않은 계정입니다. 관리자에게 문의해주세요.",
        )

    token = create_access_token(
        subject=staff.staff_id,
        organization_id=staff.organization_id,
    )
    return TokenResponse(
        access_token=token,
        organization_name=staff.organization.organization_name
    )


@router.get("/me", response_model=StaffMe)
def read_me(current_staff: Staff = Depends(get_current_staff)) -> Staff:
    return current_staff
