from sqlalchemy import Column, BigInteger, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Assignment(Base):
    __tablename__ = "assignment"

    assignment_id = Column(BigInteger, primary_key=True, autoincrement=True)
    staff_id = Column(BigInteger, ForeignKey("staff.staff_id"), nullable=False)
    client_id = Column(BigInteger, ForeignKey("client.client_id"), nullable=False)
    assistant_id = Column(BigInteger, ForeignKey("assistant.assistant_id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    assignment_status = Column(String(20), default="active")

    # Relationships
    staff = relationship("Staff", back_populates="assignments")
    client = relationship("Client", back_populates="assignments")
    assistant = relationship("Assistant", back_populates="assignments")
    service_logs = relationship("ServiceLog", back_populates="assignment")