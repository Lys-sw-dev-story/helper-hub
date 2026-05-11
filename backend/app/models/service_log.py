from sqlalchemy import Column, BigInteger, Integer, Date, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ServiceLog(Base):
    __tablename__ = "service_log"

    service_log_id = Column(BigInteger, primary_key=True, autoincrement=True)
    service_count = Column(Integer)
    service_date = Column(Date, nullable=False)
    service_hours = Column(Numeric(5, 2), nullable=False)
    service_content = Column(Text)
    assignment_id = Column(BigInteger, ForeignKey("assignment.assignment_id"), nullable=False)
    assignment = relationship("Assignment", back_populates="service_logs")