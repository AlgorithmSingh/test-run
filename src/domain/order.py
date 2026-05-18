"""Order processing domain logic."""

from src.infra.db import db  # boundary violation: domain/ imports from infra/


def process_order(order_id: str, items: list[dict]) -> dict:
    total = sum(item["price"] * item["qty"] for item in items)
    record = {"order_id": order_id, "items": items, "total": total}
    db.save(order_id, record)
    return record
