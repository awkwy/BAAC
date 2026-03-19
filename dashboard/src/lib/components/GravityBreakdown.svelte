<script>
	/**
	 * GravityBreakdown — Visual breakdown of severity outcomes.
	 * Uses a waffle chart (100 squares) to show proportions intuitively.
	 * Each square = ~1% of users. Hover a legend item to highlight that category.
	 */
	import { GRAVITY_COLORS } from '$lib/utils/format.js';

	let { distribution = {} } = $props();

	let hoveredCategory = $state(null);

	/* Use $derived so these recompute when distribution prop changes */
	let total = $derived(
		(distribution.indemne ?? 0) + (distribution.blesse_leger ?? 0) +
		(distribution.hospitalise ?? 0) + (distribution.tue ?? 0)
	);

	let categories = $derived([
		{ key: 'tue', label: 'Tué', color: GRAVITY_COLORS[2], count: distribution.tue ?? 0 },
		{ key: 'hospitalise', label: 'Hospitalisé', color: GRAVITY_COLORS[3], count: distribution.hospitalise ?? 0 },
		{ key: 'blesse_leger', label: 'Blessé léger', color: GRAVITY_COLORS[4], count: distribution.blesse_leger ?? 0 },
		{ key: 'indemne', label: 'Indemne', color: GRAVITY_COLORS[1], count: distribution.indemne ?? 0 },
	]);

	/* Build 100 cells — each cell tracks its category key for hover highlighting */
	let cells = $derived.by(() => {
		if (total === 0) return [];
		const result = [];
		for (const cat of categories) {
			const n = Math.round((cat.count / total) * 100);
			for (let i = 0; i < n; i++) {
				result.push({ color: cat.color, label: cat.label, key: cat.key });
			}
		}
		while (result.length < 100) result.push({ color: '#E2DDD4', label: '', key: 'empty' });
		return result.slice(0, 100);
	});
</script>

<div class="gravity-breakdown">
	{#if cells.length > 0}
		<div class="waffle-grid">
			{#each cells as cell, i}
				<div
					class="waffle-cell"
					class:dimmed={hoveredCategory !== null && cell.key !== hoveredCategory}
					style="background: {cell.color}; animation-delay: {i * 8}ms;"
					title={cell.label}
					role="presentation"
					onmouseenter={() => hoveredCategory = cell.key}
					onmouseleave={() => hoveredCategory = null}
				></div>
			{/each}
		</div>
	{:else}
		<p style="color: var(--text-tertiary); text-align: center;">Chargement…</p>
	{/if}

	<div class="legend-row">
		{#each categories as cat}
			{@const pctVal = total > 0 ? ((cat.count / total) * 100).toFixed(1) : '0'}
			<button
				class="legend-item"
				class:active={hoveredCategory === cat.key}
				onmouseenter={() => hoveredCategory = cat.key}
				onmouseleave={() => hoveredCategory = null}
			>
				<span class="legend-swatch" style="background: {cat.color};"></span>
				<span class="legend-text">
					<strong>{cat.count.toLocaleString('fr-FR')}</strong> {cat.label}
					<span class="legend-pct mono">({pctVal}%)</span>
				</span>
			</button>
		{/each}
	</div>
</div>

<style>
	.gravity-breakdown {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--space-lg);
	}

	.waffle-grid {
		display: grid;
		grid-template-columns: repeat(20, 1fr);
		gap: 3px;
		width: 100%;
		max-width: 520px;
		margin: 0 auto;
	}

	.waffle-cell {
		aspect-ratio: 1;
		border-radius: 3px;
		opacity: 0;
		transition: opacity 0.2s, transform 0.2s var(--ease-out);
		animation: cellAppear 0.3s var(--ease-out) forwards;
	}

	@keyframes cellAppear {
		from { opacity: 0; transform: scale(0.5); }
		to { opacity: 0.88; transform: scale(1); }
	}

	.waffle-cell:hover {
		opacity: 1 !important;
		transform: scale(1.35);
		z-index: 2;
		box-shadow: 0 2px 8px rgba(0,0,0,0.15);
	}

	.waffle-cell.dimmed {
		opacity: 0.2 !important;
		transform: scale(0.92);
	}

	.legend-row {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: var(--space-sm) var(--space-lg);
	}

	.legend-item {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 0.88rem;
		background: none;
		border: 2px solid transparent;
		border-radius: var(--radius-md);
		padding: 6px 12px;
		cursor: pointer;
		transition: all 0.2s;
		font-family: inherit;
		color: inherit;
	}

	.legend-item:hover,
	.legend-item.active {
		border-color: var(--border);
		background: var(--surface-alt);
	}

	.legend-swatch {
		width: 14px;
		height: 14px;
		border-radius: 3px;
		flex-shrink: 0;
	}

	.legend-text strong {
		font-weight: 700;
	}

	.legend-pct {
		font-size: 0.75rem;
		color: var(--text-tertiary);
	}
</style>
