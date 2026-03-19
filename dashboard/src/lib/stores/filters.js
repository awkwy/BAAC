import { writable, derived } from 'svelte/store';

/**
 * Global filter state — shared across map, charts, and panels.
 * When any filter changes, all reactive components update automatically.
 */
export const filters = writable({
	gravity: [],      // e.g. [2, 3] = only fatal + hospitalized
	lighting: [],     // e.g. [3, 4, 5] = night conditions
	weather: [],      // e.g. ['pluie']
	vehicle: [],      // e.g. ['2RM >125cm³']
	agglo: null,      // 0 = hors agglo, 1 = en agglo, null = all
	night: null,      // 0 or 1 or null
	ageGroup: [],
});

/** Reset all filters to show everything */
export function resetFilters() {
	filters.set({
		gravity: [],
		lighting: [],
		weather: [],
		vehicle: [],
		agglo: null,
		night: null,
		ageGroup: [],
	});
}

/** Track which section is currently in the viewport (for nav highlighting) */
export const activeSection = writable('hero');

/** Track if any filter is active (for showing a "reset" button) */
export const hasActiveFilters = derived(filters, ($f) => {
	return (
		$f.gravity.length > 0 ||
		$f.lighting.length > 0 ||
		$f.weather.length > 0 ||
		$f.vehicle.length > 0 ||
		$f.agglo !== null ||
		$f.night !== null ||
		$f.ageGroup.length > 0
	);
});
