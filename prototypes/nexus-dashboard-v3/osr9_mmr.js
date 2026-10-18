'use strict';
// Maximal Marginal Relevance source selection (OSR-9 L-stage). Prototype.
function cosine(a, b) {
  let d = 0, na = 0, nb = 0;
  for (let i = 0; i < a.length; i++) { d += a[i] * b[i]; na += a[i] * a[i]; nb += b[i] * b[i]; }
  return na === 0 || nb === 0 ? 0 : d / Math.sqrt(na * nb);
}

function mmrSelect(items, k, lambda = 0.7) {
  const pool = items.slice();
  const selected = [];
  while (selected.length < k && pool.length) {
    let best = -1, bestScore = -Infinity;
    pool.forEach((it, idx) => {
      const redundancy = selected.reduce((mx, s) => Math.max(mx, cosine(it.vec, s.vec)), 0);
      const score = lambda * it.relevance - (1 - lambda) * redundancy;
      if (score > bestScore) { bestScore = score; best = idx; }
    });
    selected.push(pool.splice(best, 1)[0]);
  }
  return selected;
}

if (typeof module !== 'undefined') module.exports = { mmrSelect, cosine };
