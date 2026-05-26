from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff
from app.core.database import get_db
from app.models.staff import Staff
from app.schemas.dashboard_schema import DashboardSummary
from app.services import dashboard_service


router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return dashboard_service.build_summary(
        db=db,
        organization_id=current_staff.organization_id,
        today=date.today(),
    )
