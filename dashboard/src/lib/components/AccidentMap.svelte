<script>
	import { onMount, onDestroy } from 'svelte';
	import { filters, hasActiveFilters, resetFilters } from '$lib/stores/filters.js';
	import { GRAVITY_LABELS, GRAVITY_COLORS, GRAVITY_RADIUS, LIGHTING_LABELS, ATM_LABELS, COLLISION_LABELS } from '$lib/utils/format.js';

	let { accidents = [] } = $props();

	let mapContainer;
	let map;
	let markerLayer;
	let L;

	let filteredAccidents = $derived.by(() => {
		const f = $filters;
		return accidents.filter(a => {
			if (f.gravity.length > 0 && !f.gravity.includes(a.g)) return false;
			if (f.lighting.length > 0 && !f.lighting.includes(a.lum)) return false;
			if (f.night !== null && a.nuit !== f.night) return false;
			if (f.agglo !== null) {
				const isAgglo = a.agg === 2 ? 1 : 0;
				if (isAgglo !== f.agglo) return false;
			}
			return true;
		});
	});

	let count = $derived(filteredAccidents.length);

	function buildPopup(a) {
		const gravLabel = GRAVITY_LABELS[a.g] || 'Inconnu';
		const gravColor = GRAVITY_COLORS[a.g] || '#888';
		const lumLabel = LIGHTING_LABELS[a.lum] || '—';
		const atmLabel = ATM_LABELS[a.atm] || '—';
		const colLabel = COLLISION_LABELS[a.col] || '—';

		return `
			<div style="font-family: 'Source Sans 3', sans-serif; font-size: 13px; line-height: 1.6; min-width: 180px;">
				<div style="font-weight: 700; font-size: 15px; margin-bottom: 4px;">Accident #${a.id.slice(-4)}</div>
				<div style="color: ${gravColor}; font-weight: 700; margin-bottom: 6px;">${gravLabel}</div>
				<div><strong>Véhicule :</strong> ${a.veh}</div>
				<div><strong>Heure :</strong> ${a.h || '—'}</div>
				<div><strong>Éclairage :</strong> ${lumLabel}</div>
				<div><strong>Météo :</strong> ${atmLabel}</div>
				<div><strong>Collision :</strong> ${colLabel}</div>
				<div><strong>Usagers :</strong> ${a.n}</div>
			</div>
		`;
	}

	function updateMarkers() {
		if (!markerLayer || !L) return;
		markerLayer.clearLayers();

		const sorted = [...filteredAccidents].sort((a, b) => {
			const prio = { 2: 4, 3: 3, 4: 2, 1: 1 };
			return (prio[a.g] || 0) - (prio[b.g] || 0);
		});

		for (const a of sorted) {
			if (a.lat == null || a.lon == null) continue;
			const marker = L.circleMarker([a.lat, a.lon], {
				radius: GRAVITY_RADIUS[a.g] || 5,
				fillColor: GRAVITY_COLORS[a.g] || '#888',
				color: '#fff',
				weight: 1.5,
				opacity: 0.9,
				fillOpacity: 0.75,
			});
			marker.bindPopup(buildPopup(a));
			markerLayer.addLayer(marker);
		}
	}

	$effect(() => {
		filteredAccidents; // track dependency
		updateMarkers();
	});

	onMount(async () => {
		L = (await import('leaflet')).default;

		map = L.map(mapContainer, {
			zoomControl: false,
			attributionControl: true,
		}).setView([-21.115, 55.535], 10);

		L.control.zoom({ position: 'bottomright' }).addTo(map);

		const satellite = L.tileLayer(
			'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
			{ maxZoom: 19 }
		);
		const osm = L.tileLayer(
			'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
			{ maxZoom: 19, attribution: '© OpenStreetMap' }
		);
		const topo = L.tileLayer(
			'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
			{ maxZoom: 17, attribution: '© OpenTopoMap' }
		);
		const labels = L.tileLayer(
			'https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',
			{ maxZoom: 19, opacity: 0.9 }
		);

		satellite.addTo(map);
		labels.addTo(map);

		L.control.layers(
			{ 'Satellite': satellite, 'Routes': osm, 'Relief': topo },
			{ 'Labels': labels },
			{ position: 'topright', collapsed: true }
		).addTo(map);

		markerLayer = L.layerGroup().addTo(map);
		updateMarkers();

		setTimeout(() => map.invalidateSize(), 200);
	});

	onDestroy(() => {
		if (map) map.remove();
	});
</script>

<div class="map-wrapper">
	<div class="map-container" bind:this={mapContainer}></div>

	<div class="map-counter">
		<span class="mono" style="font-size: 1.3rem; font-weight: 700; color: var(--accent);">{count}</span>
		<span style="font-size: 0.75rem; color: var(--text-tertiary);">accidents</span>
	</div>

	<div class="map-legend">
		{#each [[2, 'Mortel'], [3, 'Hospitalisé'], [4, 'Blessé léger'], [1, 'Indemne']] as [code, label]}
			<div class="legend-item">
				<span class="legend-dot" style="background: {GRAVITY_COLORS[code]}; width: {GRAVITY_RADIUS[code] * 2}px; height: {GRAVITY_RADIUS[code] * 2}px;"></span>
				<span>{label}</span>
			</div>
		{/each}
	</div>

	{#if $hasActiveFilters}
		<button class="map-reset" onclick={resetFilters}>
			✕ Réinitialiser les filtres
		</button>
	{/if}
</div>

<style>
	.map-wrapper {
		position: relative;
		width: 100%;
		height: 560px;
		border-radius: var(--radius-lg);
		overflow: hidden;
		border: 1px solid var(--border);
		box-shadow: var(--shadow-md);
	}

	.map-container {
		width: 100%;
		height: 100%;
	}

	.map-counter {
		position: absolute;
		top: 14px;
		left: 14px;
		z-index: 1000;
		background: rgba(255, 255, 255, 0.92);
		backdrop-filter: blur(8px);
		padding: 8px 16px;
		border-radius: var(--radius-md);
		border: 1px solid var(--border-light);
		display: flex;
		flex-direction: column;
		align-items: center;
		box-shadow: var(--shadow-sm);
	}

	.map-legend {
		position: absolute;
		bottom: 16px;
		left: 16px;
		z-index: 1000;
		background: rgba(255, 255, 255, 0.92);
		backdrop-filter: blur(8px);
		padding: 10px 14px;
		border-radius: var(--radius-md);
		border: 1px solid var(--border-light);
		font-size: 0.78rem;
		box-shadow: var(--shadow-sm);
	}

	.legend-item {
		display: flex;
		align-items: center;
		gap: 8px;
		margin: 3px 0;
	}

	.legend-dot {
		border-radius: 50%;
		flex-shrink: 0;
	}

	.map-reset {
		position: absolute;
		bottom: 16px;
		right: 16px;
		z-index: 1000;
		background: var(--surface);
		border: 1px solid var(--accent);
		color: var(--accent);
		font-family: var(--font-body);
		font-size: 0.82rem;
		font-weight: 600;
		padding: 8px 16px;
		border-radius: var(--radius-md);
		cursor: pointer;
		box-shadow: var(--shadow-sm);
		transition: all 0.2s;
	}

	.map-reset:hover {
		background: var(--accent);
		color: white;
	}

	:global(.leaflet-popup-content-wrapper) {
		border-radius: 10px !important;
		box-shadow: 0 8px 30px rgba(0,0,0,0.12) !important;
	}

	:global(.leaflet-popup-content) {
		margin: 12px 16px !important;
	}

	@media (max-width: 768px) {
		.map-wrapper {
			height: 420px;
			border-radius: var(--radius-md);
		}
	}
</style>
