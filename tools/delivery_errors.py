"""Shared sanitized failures for delivery and persistence gates."""


class DeliveryError(Exception):
    """Evidence-preserving failure without raw service responses or secrets."""
