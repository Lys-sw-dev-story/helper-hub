from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Staff(Base):
    __tablename__ = "staff"

    staff_id = Column(BigInteger, primary_key=True, autoincrement=True)
    staff_email = Column(String(255), unique=True, nullable=False)
    staff_password_hash = Column(String(255), nullable=False)
    staff_name = Column(String(100), nullable=False)
    staff_role = Column(String(50))
    organization_id = Column(BigInteger, ForeignKey("organization.organization_id"))

    # Relationships
    organization = relationship("Organization", back_populates="staffs")
    assignments = relationship("Assignment", back_populates="staff")