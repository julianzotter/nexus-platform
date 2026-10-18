'use strict';
// PROTOTYPE - not a certified calculation. EN 1995-1-1 Cl. 6.3.2 column buckling, rectangular section,
// single axis, pinned-pinned effective length factor supplied by caller. Human review required.
const TOLERANCE = 1.0e-9;

const MATERIALS = Object.freeze({
  C24:   Object.freeze({ fc0k: 21.0, E005: 7400, gammaM: 1.3,  betaC: 0.2 }),
  C30:   Object.freeze({ fc0k: 23.0, E005: 8000, gammaM: 1.3,  betaC: 0.2 }),
  GL24h: Object.freeze({ fc0k: 24.0, E005: 9400, gammaM: 1.25, betaC: 0.1 }),
  GL28h: Object.freeze({ fc0k: 26.5, E005: 10200, gammaM: 1.25, betaC: 0.1 }),
});

function ec5Buckling({ material, b, h, L, beta = 1.0, N, kmod = 0.8 }) {
  const m = MATERIALS[material];
  if (!m) throw new Error('Unknown material: ' + material);
  for (const [k, v] of Object.entries({ b, h, L, beta, N, kmod })) {
    if (!Number.isFinite(v) || v <= 0) throw new Error('Invalid input ' + k + ': ' + v);
  }
  const A = b * h; // mm^2
  const i = Math.min(b, h) / Math.sqrt(12); // governing (weak) axis, mm
  const lambda = (beta * L) / i;
  const lambdaRel = (lambda / Math.PI) * Math.sqrt(m.fc0k / m.E005);
  const k = 0.5 * (1 + m.betaC * (lambdaRel - 0.3) + lambdaRel ** 2);
  const kc = lambdaRel <= 0.3 ? 1 : 1 / (k + Math.sqrt(k * k - lambdaRel ** 2));
  const fc0d = (kmod * m.fc0k) / m.gammaM;
  const sigmaC = (N * 1000) / A; // N in kN -> N/mm^2
  const utilization = sigmaC / (kc * fc0d);
  const pass = utilization <= 1.0 + TOLERANCE;
  return { material, lambda, lambdaRel, kc, fc0d, sigmaC, utilization, pass,
           gate: pass ? 'PASS' : 'FAIL', status: pass ? 'KANDIDAT - PASS (no release)' : 'KANDIDAT - FAIL' };
}

if (typeof module !== 'undefined') module.exports = { ec5Buckling, MATERIALS, TOLERANCE };
