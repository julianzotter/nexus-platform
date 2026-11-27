// Data-freshness guard (ported from ID03 draft live adapter, UI-03): never show a fresh state
// for an old observation. Browser fetch time (checkedAt) is NOT observation time.
// Source of observation: nexus.monitor.observedAt (monitor run), threshold policy.staleAfterHours.
(function (root) {
  'use strict';
  const DEFAULT_STALE_HOURS = 2; // nexus-monitor runs hourly (:17 UTC); 2 h tolerates one missed run.

  function freshness(data, now) {
    const observed = data && data.nexus && data.nexus.monitor && data.nexus.monitor.observedAt;
    const configured = Number(data && data.policy && data.policy.staleAfterHours);
    const limitHours = Number.isFinite(configured) && configured > 0 ? configured : DEFAULT_STALE_HOURS;
    if (!observed || !Number.isFinite(Date.parse(observed))) {
      return { state: 'NO_DATA', ageHours: null, limitHours, observedAt: null };
    }
    const ageHours = (now - Date.parse(observed)) / 3600000;
    // Observation in the future = clock/data conflict -> not fresh.
    const state = ageHours < 0 ? 'CONFLICT' : (ageHours <= limitHours ? 'FRESH' : 'STALE');
    return { state, ageHours: Math.round(ageHours * 10) / 10, limitHours, observedAt: observed };
  }

  root.nexusFreshness = freshness;
  if (typeof module !== 'undefined' && module.exports) module.exports = { freshness, DEFAULT_STALE_HOURS };
})(typeof window !== 'undefined' ? window : globalThis);
