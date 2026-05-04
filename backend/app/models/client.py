from sqlalchemy import Column, BigInteger, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Client(Base):
    __tablename__ = "client"

    client_id = Column(BigInteger, primary_key=True, autoincrement=True)
    client_name = Column(String(100), nullable=False)
    client_birth_date = Column(Date)
    client_phone = Column(String(30))
    client_address = Column(String(255))
    client_status = Column(String(255))
    client_memo = Column(Text)
    organization_id = Column(BigInteger, ForeignKey("organization.organization_id"))

    # Relationships
    organization = relationship("Organization", back_populates="clients")
    assignments = relationship("Assignment", back_populates="client")