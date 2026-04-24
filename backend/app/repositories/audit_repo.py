from app.extensions import db
from app.models.audit import AuditLog


def log(
    entity_type: str,
    entity_id: int | None,
    action: str,
    actor_user_id: int | None = None,
    extra: dict | None = None,
    ip: str | None = None,
) -> AuditLog:
    entry = AuditLog(
        actor_user_id=actor_user_id,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        extra=extra,
        ip=ip,
    )
    db.session.add(entry)
    db.session.flush()
    return entry
