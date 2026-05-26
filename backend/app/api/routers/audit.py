from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff
from app.core.database import get_db
from app.models.staff import Staff
from app.schemas.audit_schema import AuditOverview, AuditRecentResponse
from app.services import audit_service


router = APIRouter()


@router.get("/overview", response_model=AuditOverview)
def get_audit_overview(
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return audit_service.build_overview(
        db=db,
        organization_id=current_staff.organization_id,
        today=date.today(),
    )


@router.get("/recent", response_model=AuditRecentResponse)
def get_audit_recent(
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return audit_service.build_recent(
        db=db,
        organization_id=current_staff.organization_id,
        today=date.today(),
    )
