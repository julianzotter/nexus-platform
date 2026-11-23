"""Strict JSON contract loader. Decimals are decimal strings, never floats."""
from __future__ import annotations
import json
import re
from dataclasses import MISSING, fields, is_dataclass
from decimal import Decimal
from types import UnionType
from typing import Literal, TypeVar, Union, cast, get_args, get_origin, get_type_hints
from nexus.domain.contracts.base import Contract, ContractError, check_type, require
from nexus.domain.contracts.exchange import ImportedModel, MappingReport
from nexus.domain.contracts.model import AnalysisModel
from nexus.domain.services.canonical import canonical_bytes

T = TypeVar("T", bound=Contract)
DECIMAL_PATTERN = r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?$"


def no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def no_json_float(value: str) -> object:
    raise ContractError(f"JSON floating-point token forbidden; use decimal strings: {value}")


def decode(value: object, annotation: object) -> object:
    origin, args = get_origin(annotation), get_args(annotation)
    if origin in (Union, UnionType):
        for alternative in args:
            try:
                return decode(value, alternative)
            except (ContractError, TypeError):
                pass
        raise ContractError("no matching JSON union variant")
    if origin is tuple:
        require(type(value) is list, "JSON array required")
        assert isinstance(value, list)
        if len(args) == 2 and args[1] is Ellipsis:
            return tuple(decode(item, args[0]) for item in value)
        require(len(value) == len(args), "wrong JSON array length")
        return tuple(decode(item, kind) for item, kind in zip(value, args))
    if annotation is Decimal:
        require(isinstance(value, str) and re.fullmatch(DECIMAL_PATTERN, value) is not None,
                "decimal string required")
        return Decimal(cast(str, value))
    if isinstance(annotation, type) and is_dataclass(annotation):
        return decode_dataclass(value, annotation)
    check_type(value, annotation, "JSON value")
    return value


def decode_dataclass(value: object, annotation: type[object]) -> object:
    require(type(value) is dict, "JSON object required")
    assert isinstance(value, dict)
    if not is_dataclass(annotation):
        raise ContractError("dataclass type required")
    contract_fields = fields(annotation)
    allowed = {field.name for field in contract_fields}
    require(set(value) <= allowed, f"unknown fields: {sorted(set(value)-allowed)}")
    needed = {field.name for field in contract_fields
              if field.default is MISSING and field.default_factory is MISSING}
    require(needed <= set(value), f"missing fields: {sorted(needed-set(value))}")
    hints = get_type_hints(annotation)
    kwargs = {key: decode(item, hints[key]) for key, item in value.items()}
    return annotation(**kwargs)


def loads_contract(raw: bytes, contract_type: type[T]) -> T:
    payload: object = json.loads(raw, object_pairs_hook=no_duplicates,
                                parse_float=no_json_float, parse_constant=no_json_float)
    return cast(T, decode(payload, contract_type))


class JsonModelExchange:
    """Identity-preserving analytical JSON exchange, not IFC/DWG conversion."""
    def read(self, source: bytes) -> ImportedModel:
        model = loads_contract(source, AnalysisModel)
        return ImportedModel(model, MappingReport("nexus-json/0.1", model.schema_version, ()))

    def write(self, model: AnalysisModel) -> tuple[bytes, MappingReport]:
        return canonical_bytes(model), MappingReport(model.schema_version, "nexus-json/0.1", ())
