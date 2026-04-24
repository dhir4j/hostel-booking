"""Pagination helper for SQLAlchemy 2.0 ``select()`` queries."""

from __future__ import annotations

import math
from typing import Any, Tuple

from sqlalchemy import func, select
from sqlalchemy.sql import Select

from app.extensions import db


def paginate(
    query: Select,
    page: int,
    per_page: int,
    max_per_page: int = 100,
) -> Tuple[list[Any], dict]:
    """Paginate a SQLAlchemy 2.0 ``select()`` statement.

    Args:
        query: A ``select(Model)`` statement. Must NOT have a pre-applied
            ``LIMIT/OFFSET``; this function applies them.
        page: 1-based page index. Values < 1 are clamped to 1.
        per_page: Requested page size. Values < 1 clamp to 1; values above
            ``max_per_page`` clamp to ``max_per_page``.
        max_per_page: Upper bound on page size to protect the DB.

    Returns:
        ``(items, meta)`` where ``meta`` contains ``page``, ``per_page``,
        ``total``, ``total_pages``, ``has_next``, ``has_prev``.
    """
    # Clamp inputs defensively; route-level schemas should already validate.
    page = max(1, int(page or 1))
    per_page = max(1, min(int(per_page or 1), max_per_page))

    # Total count: wrap original query as a subquery so ordering / joins are
    # preserved but we only pull COUNT(*).
    count_stmt = select(func.count()).select_from(query.order_by(None).subquery())
    total: int = db.session.execute(count_stmt).scalar_one() or 0

    total_pages = math.ceil(total / per_page) if total else 0

    offset = (page - 1) * per_page
    page_stmt = query.limit(per_page).offset(offset)
    items = list(db.session.execute(page_stmt).scalars().all())

    meta = {
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
    return items, meta


__all__ = ["paginate"]
