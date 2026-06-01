from datetime import date, timedelta
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.core.constants import (
    AUDIT_WINDOW_YEARS,
    EXPIRATION_WARNING_DAYS,
    RETENTION_YEARS,
    DocumentStatus,
    DocumentTargetType,
)
from app.models.assignment import Assignment
from app.models.assistant import Assistant
from app.models.client import Client
from app.models.document import Document
from app.models.document_requirement import DocumentRequirement
from app.models.service_log import ServiceLog
from app.schemas.audit_schema import (
    AuditDocumentItem,
    AuditOverview,
    AuditRecentAssistant,
    AuditRecentClient,
    AuditRecentResponse,
    AuditRecentServiceLog,
)
from app.services.document_service import compute_status


def _shift_years(reference: date, years: int) -> date:
    """단순 연 차감/가산. 윤년이면 day=28 로 떨어뜨린다."""
    try:
        return reference.replace(year=reference.year - years)
    except ValueError:
        return reference.replace(year=reference.year - years, day=28)


def _retention_until(created: Optional[date]) -> Optional[date]:
    if created is None:
        return None
    try:
        return created.replace(year=created.year + RETENTION_YEARS)
    except ValueError:
        return created.replace(year=created.year + RETENTION_YEARS, day=28)


def _days_between(a: Optional[date], b: date) -> Optional[int]:
    if a is None:
        return None
    return (a - b).days


def _target_name_maps(db: Session, organization_id: int) -> dict[str, dict[int, str]]:
    clients = (
        db.query(Client.client_id, Client.client_name)
        .filter(Client.organization_id == organization_id)
        .all()
    )
    assistants = (
        db.query(Assistant.assistant_id, Assistant.assistant_name)
        .filter(Assistant.organization_id == organization_id)
        .all()
    )
    return {
        DocumentTargetType.CLIENT.value: {cid: name for cid, name in clients},
        DocumentTargetType.ASSISTANT.value: {aid: name for aid, name in assistants},
    }


def _doc_to_item(
    doc: Document, target_name: str, today: date
) -> AuditDocumentItem:
    status = compute_status(doc, today)
    retention_until = _retention_until(doc.created_date)
    return AuditDocumentItem(
        document_id=doc.document_id,
        requirement_id=doc.requirement_id,
        document_name=doc.requirement.document_name,
        target_type=DocumentTargetType(doc.requirement.target_type),
        target_id=doc.target_id,
        target_name=target_name,
        created_date=doc.created_date,
        expiration_date=doc.expiration_date,
        retention_until=retention_until,
        status=status,
        days_until_expire=_days_between(doc.expiration_date, today),
        days_until_retention_end=_days_between(retention_until, today),
    )


def _missing_items(
    db: Session, organization_id: int, today: date
) -> list[AuditDocumentItem]:
    """target_type 별 모든 entity 에 대해, requirement 가 있는데 document 가 없는 항목."""
    name_maps = _target_name_maps(db, organization_id)

    client_reqs = (
        db.query(DocumentRequirement)
        .filter(DocumentRequirement.target_type == DocumentTargetType.CLIENT.value)
        .all()
    )
    assistant_reqs = (
        db.query(DocumentRequirement)
        .filter(DocumentRequirement.target_type == DocumentTargetType.ASSISTANT.value)
        .all()
    )

    existing = {
        (doc.target_id, doc.requirement_id)
        for doc in db.query(Document.target_id, Document.requirement_id)
        .filter(Document.organization_id == organization_id)
        .all()
    }

    items: list[AuditDocumentItem] = []
    for target_id, target_name in name_maps[DocumentTargetType.CLIENT.value].items():
        for req in client_reqs:
            if (target_id, req.requirement_id) in existing:
                continue
            items.append(
                AuditDocumentItem(
                    document_id=None,
                    requirement_id=req.requirement_id,
                    document_name=req.document_name,
                    target_type=DocumentTargetType.CLIENT,
                    target_id=target_id,
                    target_name=target_name,
                    created_date=None,
                    expiration_date=None,
                    retention_until=None,
                    status=DocumentStatus.NOT_SUBMITTED,
                    days_until_expire=None,
                    days_until_retention_end=None,
                )
            )
    for target_id, target_name in name_maps[DocumentTargetType.ASSISTANT.value].items():
        for req in assistant_reqs:
            if (target_id, req.requirement_id) in existing:
                continue
            items.append(
                AuditDocumentItem(
                    document_id=None,
                    requirement_id=req.requirement_id,
                    document_name=req.document_name,
                    target_type=DocumentTargetType.ASSISTANT,
                    target_id=target_id,
                    target_name=target_name,
                    created_date=None,
                    expiration_date=None,
                    retention_until=None,
                    status=DocumentStatus.NOT_SUBMITTED,
                    days_until_expire=None,
                    days_until_retention_end=None,
                )
            )
    return items


def _load_org_documents(db: Session, organization_id: int) -> list[Document]:
    return (
        db.query(Document)
        .options(joinedload(Document.requirement))
        .filter(Document.organization_id == organization_id)
        .all()
    )


def build_overview(
    db: Session, organization_id: int, today: date
) -> AuditOverview:
    name_maps = _target_name_maps(db, organization_id)
    docs = _load_org_documents(db, organization_id)

    expiring_soon: list[AuditDocumentItem] = []
    retention_ending_soon: list[AuditDocumentItem] = []

    retention_warn_until = today + timedelta(days=EXPIRATION_WARNING_DAYS)

    missing = _missing_items(db, organization_id, today)

    for doc in docs:
        if doc.requirement is None:
            continue
        target_name = name_maps.get(doc.requirement.target_type, {}).get(
            doc.target_id, "(이름 없음)"
        )
        item = _doc_to_item(doc, target_name, today)

        if item.status == DocumentStatus.EXPIRING_SOON:
            expiring_soon.append(item)
        elif item.status == DocumentStatus.NOT_SUBMITTED:
            missing.append(item)

        retention_until = item.retention_until
        if (
            retention_until is not None
            and today <= retention_until <= retention_warn_until
        ):
            retention_ending_soon.append(item)

    return AuditOverview(
        missing=missing,
        expiring_soon=sorted(
            expiring_soon, key=lambda i: (i.expiration_date or date.max)
        ),
        retention_ending_soon=sorted(
            retention_ending_soon, key=lambda i: (i.retention_until or date.max)
        ),
    )


def build_recent(
    db: Session, organization_id: int, today: date
) -> AuditRecentResponse:
    cutoff = _shift_years(today, AUDIT_WINDOW_YEARS)

    clients = (
        db.query(Client)
        .filter(Client.organization_id == organization_id)
        .all()
    )
    assistants = (
        db.query(Assistant)
        .filter(Assistant.organization_id == organization_id)
        .all()
    )

    # 최근 2년 이내 문서 (created_date >= cutoff)
    docs = (
        db.query(Document)
        .options(joinedload(Document.requirement))
        .filter(
            Document.organization_id == organization_id,
            Document.created_date.isnot(None),
            Document.created_date >= cutoff,
        )
        .order_by(Document.created_date.desc())
        .all()
    )

    name_maps = _target_name_maps(db, organization_id)
    document_items = [
        _doc_to_item(
            doc,
            name_maps.get(doc.requirement.target_type, {}).get(
                doc.target_id, "(이름 없음)"
            ),
            today,
        )
        for doc in docs
        if doc.requirement is not None
    ]

    service_logs = (
        db.query(ServiceLog)
        .join(Assignment, ServiceLog.assignment_id == Assignment.assignment_id)
        .join(Client, Assignment.client_id == Client.client_id)
        .filter(
            Client.organization_id == organization_id,
            ServiceLog.service_date >= cutoff,
        )
        .options(
            joinedload(ServiceLog.assignment).joinedload(Assignment.client),
            joinedload(ServiceLog.assignment).joinedload(Assignment.assistant),
        )
        .order_by(ServiceLog.service_date.desc())
        .all()
    )
    service_log_items = [
        AuditRecentServiceLog(
            service_log_id=log.service_log_id,
            assignment_id=log.assignment_id,
            service_date=log.service_date,
            service_hours=log.service_hours,
            service_count=log.service_count,
            service_content=log.service_content,
            client_id=log.assignment.client_id,
            client_name=log.assignment.client.client_name,
            assistant_id=log.assignment.assistant_id,
            assistant_name=log.assignment.assistant.assistant_name,
        )
        for log in service_logs
    ]

    # 이용자/활동지원사 자체는 등록일이 모델에 없으므로 organization 의 모든 항목을 그대로 노출하고
    # cutoff 정보는 응답에 포함해 프론트가 보조 표시할 수 있도록 한다.
    return AuditRecentResponse(
        window_years=AUDIT_WINDOW_YEARS,
        cutoff_date=cutoff,
        retention_years=RETENTION_YEARS,
        clients=[
            AuditRecentClient(
                client_id=c.client_id,
                client_name=c.client_name,
                client_status=c.client_status,
                organization_id=c.organization_id,
            )
            for c in clients
        ],
        assistants=[
            AuditRecentAssistant(
                assistant_id=a.assistant_id,
                assistant_name=a.assistant_name,
                work_start_date=a.work_start_date,
                organization_id=a.organization_id,
            )
            for a in assistants
        ],
        documents=document_items,
        service_logs=service_log_items,
    )
