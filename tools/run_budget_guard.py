#!/usr/bin/env python3
"""Read-only gate for a complete request measured by its actual provider adapter.

Does not tokenize, invoke a model, authorize execution, or validate external
measurement authenticity. The trusted adapter must bind its measurement to
exact request bytes and identify the model and count source.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

REQUIRED_COUNTS = (
    'context_limit', 'input_tokens', 'output_reserve', 'tool_reserve',
    'safety_margin',
)


def assess(request: bytes, receipt: dict[str, Any]) -> dict[str, Any]:
    """Check arithmetic and identity; unknown or estimated data never pass."""
    digest = hashlib.sha256(request).hexdigest()
    reasons: list[str] = []
    if not request:
        reasons.append('EMPTY_REQUEST')
    for key in ('provider', 'model_id', 'tokenizer_or_count_api', 'measurement_ref'):
        if not isinstance(receipt.get(key), str) or not receipt[key].strip():
            reasons.append(f'MISSING_{key.upper()}')
    if receipt.get('measurement_kind') != 'EXACT_FULL_REQUEST':
        reasons.append('EXACT_FULL_REQUEST_REQUIRED')
    if receipt.get('request_sha256') != digest:
        reasons.append('REQUEST_HASH_MISMATCH')
    for key in REQUIRED_COUNTS:
        value = receipt.get(key)
        if type(value) is not int or value < 0:
            reasons.append(f'INVALID_{key.upper()}')
    if reasons:
        return {'status': 'BLOCKED', 'reasons': reasons, 'request_sha256': digest,
                'measurement_authenticity': 'NOT_VERIFIED_BY_GUARD'}
    cap = receipt['context_limit']
    reserves = sum(receipt[k] for k in REQUIRED_COUNTS[2:])
    limit = cap - reserves
    if (cap <= 0 or receipt['input_tokens'] <= 0 or
            receipt['output_reserve'] <= 0 or receipt['safety_margin'] <= 0):
        reasons.append('NONPOSITIVE_LIMIT_OR_REQUIRED_RESERVE')
    if receipt['input_tokens'] > limit:
        reasons.append('CONTEXT_BUDGET_EXCEEDED')
    return {'status': 'BLOCKED' if reasons else 'PASS_BUDGET_ARITHMETIC',
            'reasons': reasons, 'request_sha256': digest,
            'input_budget': limit, 'remaining_tokens': limit - receipt['input_tokens'],
            'measurement_authenticity': 'NOT_VERIFIED_BY_GUARD'}


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate receipt key: {key}')
        result[key] = value
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    args = parser.parse_args()
    try:
        receipt = json.loads(args.receipt.read_text(encoding='utf-8'),
                             object_pairs_hook=unique_object)
        if not isinstance(receipt, dict):
            raise ValueError('receipt must be an object')
        result = assess(args.request.read_bytes(), receipt)
    except (OSError, ValueError) as exc:
        result = {'status': 'BLOCKED', 'reasons': [type(exc).__name__]}
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status'] == 'PASS_BUDGET_ARITHMETIC' else 2


if __name__ == '__main__':
    raise SystemExit(main())
