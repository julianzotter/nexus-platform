"""JSON Schema Draft 2020-12 generated from the same dataclass annotations."""
from __future__ import annotations
from dataclasses import MISSING, fields, is_dataclass
from decimal import Decimal
from types import UnionType
from typing import Literal, Union, get_args, get_origin, get_type_hints
from nexus.domain.contracts.base import Contract, ContractError
from .json_codec import DECIMAL_PATTERN


def type_schema(annotation: object, definitions: dict[str, object]) -> dict[str, object]:
    origin, args = get_origin(annotation), get_args(annotation)
    if origin in (UnionType, Union):
        return {"anyOf": [type_schema(kind, definitions) for kind in args]}
    if origin is Literal:
        return {"enum": list(args)}
    if origin is tuple:
        if len(args) == 2 and args[1] is Ellipsis:
            return {"type": "array", "items": type_schema(args[0], definitions)}
        return {"type": "array", "prefixItems": [type_schema(a, definitions) for a in args],
                "minItems": len(args), "maxItems": len(args)}
    if annotation is Decimal:
        return {"type": "string", "pattern": DECIMAL_PATTERN,
                "description": "Finite base-10 Decimal. Unit is fixed by the field/contract."}
    primitives = {str: "string", int: "integer", bool: "boolean", type(None): "null"}
    if annotation in primitives:
        return {"type": primitives[annotation]}
    if isinstance(annotation, type) and is_dataclass(annotation):
        name = annotation.__name__
        if name not in definitions:
            definitions[name] = {}
            hints = get_type_hints(annotation)
            properties = {f.name: type_schema(hints[f.name], definitions) for f in fields(annotation)}
            required = [f.name for f in fields(annotation)
                        if f.default is MISSING and f.default_factory is MISSING]
            definitions[name] = {"type": "object", "additionalProperties": False,
                                 "properties": properties, "required": required}
        return {"$ref": f"#/$defs/{name}"}
    raise ContractError(f"unsupported schema annotation: {annotation}")


def export_schema(contract_type: type[Contract]) -> dict[str, object]:
    definitions: dict[str, object] = {}
    root = type_schema(contract_type, definitions)
    return {"$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": f"urn:nexus:aec:contracts:0.1:{contract_type.__name__}",
            "title": contract_type.__name__,
            "$comment": "Structural validation only; Python domain invariants are also mandatory.",
            **root, "$defs": definitions}
