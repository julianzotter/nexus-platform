"""NEXUS-C14N/0.1: explicit local profile, not RFC 8785/JCS."""
from __future__ import annotations
import hashlib
import json
from dataclasses import fields, is_dataclass
from decimal import Decimal
from typing import TypeAlias
from nexus.domain.contracts.base import ContractError, require

Json: TypeAlias = None | bool | int | str | list["Json"] | dict[str, "Json"]
PROFILE = "nexus-c14n/0.1"


def decimal_text(value: Decimal) -> str:
    require(value.is_finite(), "finite Decimal required")
    if value == 0:
        return "0"
    result = format(value, "f")
    return result.rstrip("0").rstrip(".") if "." in result else result


def to_payload(value: object) -> Json:
    if isinstance(value, Decimal):
        return decimal_text(value)
    if is_dataclass(value) and not isinstance(value, type):
        return {field.name: to_payload(getattr(value, field.name)) for field in fields(value)}
    if type(value) is tuple:
        return [to_payload(item) for item in value]
    if value is None or type(value) in (bool, int, str):
        assert value is None or isinstance(value, (bool, int, str))
        return value
    raise ContractError(f"non-contract value cannot be canonicalized: {type(value).__name__}")


def canonical_bytes(value: object) -> bytes:
    return json.dumps(to_payload(value), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def content_hash(value: object) -> str:
    """All fields, including identity/revision/request; tuple order is significant."""
    return hashlib.sha256(PROFILE.encode("ascii") + b"\x00" + canonical_bytes(value)).hexdigest()
