"""Strict runtime validation using standard-library types only."""
from __future__ import annotations

from dataclasses import fields, is_dataclass
from decimal import Decimal
from types import UnionType
from typing import Literal, Union, get_args, get_origin, get_type_hints


class ContractError(ValueError):
    """A contract or cross-reference is invalid."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def check_type(value: object, annotation: object, path: str) -> None:
    origin, args = get_origin(annotation), get_args(annotation)
    if origin in (UnionType, Union):
        for alternative in args:
            try:
                check_type(value, alternative, path)
                return
            except ContractError:
                pass
        raise ContractError(f"{path}: no matching union variant")
    if origin is Literal:
        require(any(type(value) is type(x) and value == x for x in args),
                f"{path}: invalid literal")
    elif origin is tuple:
        require(type(value) is tuple, f"{path}: immutable tuple required")
        assert isinstance(value, tuple)
        if len(args) == 2 and args[1] is Ellipsis:
            for item in value:
                check_type(item, args[0], path)
        else:
            require(len(value) == len(args), f"{path}: wrong tuple length")
            for item, expected in zip(value, args):
                check_type(item, expected, path)
    elif annotation is type(None):
        require(value is None, f"{path}: null required")
    elif isinstance(annotation, type):
        require(type(value) is annotation, f"{path}: expected {annotation.__name__}")
        if isinstance(value, Decimal):
            require(value.is_finite(), f"{path}: finite Decimal required")
    else:
        raise ContractError(f"{path}: unsupported contract annotation")


class Contract:
    """Dataclass subclasses validate actual constructor values, not hints alone."""
    __slots__ = ()

    def __post_init__(self) -> None:
        if not is_dataclass(self):
            raise ContractError("Contract must be a dataclass")
        hints = get_type_hints(type(self))
        for field in fields(self):
            check_type(getattr(self, field.name), hints[field.name], field.name)
        self._validate()

    def _validate(self) -> None:
        """Additional semantic invariants, overridden by concrete contracts."""


def identifier(value: str) -> None:
    require(bool(value) and value == value.strip(), "nonempty trimmed identifier required")


def unique_ids(items: tuple[object, ...], name: str) -> set[str]:
    ids = [str(getattr(item, "id")) for item in items]
    require(len(ids) == len(set(ids)), f"{name}: duplicate IDs")
    return set(ids)


def sha256_text(value: str) -> None:
    require(len(value) == 64 and all(c in "0123456789abcdef" for c in value),
            "lowercase SHA-256 hex required")
