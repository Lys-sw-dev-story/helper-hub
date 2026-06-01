import sys
from app.core.database import SessionLocal
from app.models import (  # noqa: F401
    assignment,
    assistant,
    client,
    document,
    document_requirement,
    organization,
    service_log,
    staff,
)

def reset_docs():
    db = SessionLocal()
    try:
        db.query(document.Document).delete()
        db.query(document_requirement.DocumentRequirement).delete()
        db.commit()
        print("Cleared documents and requirements.")
    except Exception as e:
        db.rollback()
        print(f"Failed to clear: {e}", file=sys.stderr)
    finally:
        db.close()

if __name__ == "__main__":
    reset_docs()