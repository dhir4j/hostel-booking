from flask import request, g
from app.repositories import audit_repo

def record(entity_type: str, entity_id: int | None, action: str,
           actor_user_id: int | None = None, extra: dict | None = None) -> None:
    """Record an audit log entry. Joins caller's transaction."""
    if actor_user_id is None:
        actor_user_id = g.get('current_user_id')
    ip = None
    try:
        ip = request.remote_addr
    except RuntimeError:
        pass
    audit_repo.log(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        actor_user_id=actor_user_id,
        extra=extra,
        ip=ip,
    )
