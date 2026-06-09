from sqlalchemy import Column, BigInteger, String, Date, Boolean, Text, ForeignKey
from sqlalchemy.dialects.mysql import LONGBLOB
from sqlalchemy.orm import deferred, relationship
from app.core.database import Base

class Document(Base):
    __tablename__ = "document"

    document_id = Column(BigInteger, primary_key=True, autoincrement=True)
    target_id = Column(BigInteger, nullable=False)  # client_id 또는 assistant_id
    file_path = Column(String(500))  # 레거시(파일시스템) 경로 — 신규 업로드는 file_data 사용
    file_name = Column(String(255))  # 원본 파일명 (다운로드 시 사용)
    # 실제 파일 바이트를 DB에 저장 (팀 결정 2026-06-02: 파일시스템 대신 DB 저장).
    # 목록/체크리스트 조회 시 매번 끌어오지 않도록 deferred 로 지연 로딩한다.
    file_data = deferred(Column(LONGBLOB))
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