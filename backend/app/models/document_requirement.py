from sqlalchemy import Column, BigInteger, String, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base

class DocumentRequirement(Base):
    __tablename__ = "document_requirement"

    requirement_id = Column(BigInteger, primary_key=True, autoincrement=True)
    target_type = Column(String(20), nullable=False)  # 예: 'client', 'assistant'
    document_name = Column(String(100), nullable=False)
    valid_period_years = Column(Integer)

    # Relationships
    documents = relationship("Document", back_populates="requirement")