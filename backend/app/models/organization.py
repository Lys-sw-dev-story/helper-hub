from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Organization(Base):
    __tablename__ = "organization"

    organization_id = Column(BigInteger, primary_key=True, autoincrement=True)
    organization_name = Column(String(100), nullable=False)

    # Relationships
    staffs = relationship("Staff", back_populates="organization")
    clients = relationship("Client", back_populates="organization")
    assistants = relationship("Assistant", back_populates="organization")
    documents = relationship("Document", back_populates="organization")