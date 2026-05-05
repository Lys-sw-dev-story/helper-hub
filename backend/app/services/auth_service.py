from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.staff import Staff


def authenticate_staff(db: Session, email: str, password: str) -> Staff | None:
    staff = db.query(Staff).filter(Staff.staff_email == email).first()
    if staff is None:
        return None
    if not verify_password(password, staff.staff_password_hash):
        return None
    return staff


def get_staff_by_id(db: Session, staff_id: int) -> Staff | None:
    return db.query(Staff).filter(Staff.staff_id == staff_id).first()
