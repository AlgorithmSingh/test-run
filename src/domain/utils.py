"""Domain utility helpers."""


def format_order_id(order_id: str) -> str:
    """Format an order id for display. Not currently called anywhere."""
    return f"ORD-{order_id.upper()}"
