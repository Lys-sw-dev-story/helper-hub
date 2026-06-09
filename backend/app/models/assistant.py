from sqlalchemy import Column, BigInteger, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Assistant(Base):
    __tablename__ = "assistant"

    assistant_id = Column(BigInteger, primary_key=True, autoincrement=True)
    assistant_name = Column(String(100), nullable=False)
    assistant_phone = Column(String(30))
    work_days = Column(String(50))  # 매칭 태그: 근무 가능 요일 (CSV: "월,수,금")
    assistant_support_types = Column(String(100))  # 매칭 태그: 가능 지원 분야 (CSV)
    work_start_date = Column(Date)
    assistant_license = Column(Text)
    assistant_memo = Column(Text)
    organization_id = Column(BigInteger, ForeignKey("organization.organization_id"))

    # Relationships
    organization = relationship("Organization", back_populates="assistants")
    assignments = relationship("Assignment", back_populates="assistant")