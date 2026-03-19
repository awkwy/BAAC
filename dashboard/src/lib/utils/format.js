/**
 * Formatting utilities for the dashboard.
 * French-locale number formatting, BAAC code → label mappings,
 * and color schemes for severity levels.
 */

/* ── Number formatting ─────────────────────────────────── */

/** Format a number with French locale (spaces as thousand separators) */
export function fmt(n) {
	if (n == null || isNaN(n)) return '—';
	return n.toLocaleString('fr-FR');
}

/** Format a percentage with 1 decimal */
export function pct(n, decimals = 1) {
	if (n == null || isNaN(n)) return '—';
	return n.toFixed(decimals).replace('.', ',') + ' %';
}

/** Format an odds ratio with confidence interval */
export function fmtOR(or, ciLo, ciHi) {
	return `${or.toFixed(2)} [${ciLo.toFixed(2)} – ${ciHi.toFixed(2)}]`;
}

/* ── BAAC Gravity codes ────────────────────────────────── */

export const GRAVITY_LABELS = {
	1: 'Indemne',
	2: 'Tué',
	3: 'Hospitalisé',
	4: 'Blessé léger',
};

export const GRAVITY_COLORS = {
	1: '#6B9BD2',  // blue-ish for indemne
	2: '#C73E1D',  // red for fatal
	3: '#D4960A',  // amber for hospitalized
	4: '#2D8A56',  // green for light injury
};

export const GRAVITY_RADIUS = {
	1: 4,
	2: 9,
	3: 7,
	4: 5,
};

/* ── BAAC Lighting codes ───────────────────────────────── */

export const LIGHTING_LABELS = {
	1: 'Jour',
	2: 'Crépuscule',
	3: 'Nuit sans éclairage',
	4: 'Nuit — éclairage éteint',
	5: 'Nuit — éclairage allumé',
};

/* ── BAAC Atmospheric codes ────────────────────────────── */

export const ATM_LABELS = {
	1: 'Normale',
	2: 'Pluie légère',
	3: 'Pluie forte',
	4: 'Neige / grêle',
	5: 'Brouillard',
	6: 'Vent fort',
	7: 'Éblouissement',
	8: 'Couvert',
};

/* ── BAAC Collision codes ──────────────────────────────── */

export const COLLISION_LABELS = {
	1: 'Frontale',
	2: 'Arrière',
	3: 'Côté',
	4: 'En chaîne',
	5: 'Multiples',
	6: 'Autre',
	7: 'Sans collision',
};

/* ── Vehicle type short labels ─────────────────────────── */

export const VEHICLE_ICONS = {
	'voiture': '🚗',
	'2RM >125cm³': '🏍️',
	'2RM 50-125cm³': '🏍️',
	'2RM ≤50cm³': '🛵',
	'vélo/VAE': '🚲',
	'EDP (trottinette)': '🛴',
	'utilitaire': '🚐',
	'poids lourd': '🚛',
	'bus/car': '🚌',
	'autre': '❓',
};

/* ── Color utilities ───────────────────────────────────── */

/** Return a color based on a severity rate (0 to 1) */
export function severityColor(rate) {
	if (rate > 0.35) return 'var(--danger)';
	if (rate > 0.18) return 'var(--warn)';
	return 'var(--safe)';
}

/** Significance stars from p-value */
export function sigStars(p) {
	if (p < 0.001) return '***';
	if (p < 0.01) return '**';
	if (p < 0.05) return '*';
	return 'ns';
}

/* ── Month labels (French) ─────────────────────────────── */

export const MONTHS_FR = [
	'', 'Jan.', 'Fév.', 'Mars', 'Avr.', 'Mai', 'Juin',
	'Juil.', 'Août', 'Sep.', 'Oct.', 'Nov.', 'Déc.'
];
