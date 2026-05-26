from sqlalchemy import Column, BigInteger, String, Date, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Document(Base):
    __tablename__ = "document"

    document_id = Column(BigInteger, primary_key=True, autoincrement=True)
    target_id = Column(BigInteger, nullable=False)  # client_id 또는 assistant_id
    file_path = Column(String(500))
    created_date = Column(Date)
    expiration_date = Column(Date)
    is_submitted = Column(Boolean, default=False)
    needs_revision = Column(Boolean, default=False, nullable=False)
    document_memo = Column(Text)
    requirement_id = Column(BigInteger, ForeignKey("document_requirement.requirement_id"), nullable=False)
    organization_id = Column(BigInteger, ForeignKey("organization.organization_id"), nullable=False)

    # Relationships
    requirement = relationship("DocumentRequirement", back_populates="documents")
    organization = relationship("Organization", back_populates="documents")