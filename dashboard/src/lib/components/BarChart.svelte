<script>
	/**
	 * BarChart — a reusable horizontal bar chart component.
	 * Shows ranked items with proportional bars, values, and optional severity coloring.
	 *
	 * Props:
	 *   title:  string — chart heading
	 *   items:  Array of { label, value, total?, rate? }
	 *   colorFn: (item) => CSS color string (optional, defaults to accent)
	 *   showRate: boolean — if true, shows % rate instead of raw count
	 *   maxItems: number — cap the displayed items
	 *   note:   string — footer note
	 */
	import { fmt, pct } from '$lib/utils/format.js';

	let {
		title = '',
		items = [],
		colorFn = () => 'var(--accent)',
		showRate = false,
		maxItems = 10,
		note = '',
	} = $props();

	/* Trim to maxItems and compute proportional widths */
	let displayItems = $derived(items.slice(0, maxItems));
	let maxValue = $derived(Math.max(...displayItems.map(d => showRate ? (d.rate ?? 0) : d.value), 1));
</script>

<div class="bar-chart card">
	{#if title}
		<h4 class="bar-chart-title">{title}</h4>
	{/if}

	<div class="bar-rows">
		{#each displayItems as item, i}
			{@const val = showRate ? (item.rate ?? 0) : item.value}
			{@const widthPct = (val / maxValue) * 100}
			<div class="bar-row">
				<span class="bar-label">{item.label}</span>
				<div class="bar-track">
					<div
						class="bar-fill"
						style="width: {widthPct}%; background: {colorFn(item)};"
					></div>
				</div>
				<span class="bar-value mono">
					{showRate ? pct(val) : fmt(val)}
				</span>
			</div>
		{/each}
	</div>

	{#if note}
		<p class="bar-note">{note}</p>
	{/if}
</div>

<style>
	.bar-chart {
		padding: var(--space-lg);
	}

	.bar-chart-title {
		font-family: var(--font-body);
		font-size: 0.82rem;
		font-weight: 600;
		color: var(--text-secondary);
		text-transform: uppercase;
		letter-spacing: 0.04em;
		margin-bottom: var(--space-md);
	}

	.bar-rows {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	.bar-row {
		display: flex;
		align-items: center;
		gap: 10px;
		font-size: 0.88rem;
	}

	.bar-label {
		width: 140px;
		flex-shrink: 0;
		text-align: right;
		color: var(--text-secondary);
		font-size: 0.82rem;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.bar-track {
		flex: 1;
		height: 18px;
		background: var(--surface-alt);
		border-radius: 3px;
		overflow: hidden;
	}

	.bar-fill {
		height: 100%;
		border-radius: 3px;
		transition: width 0.6s var(--ease-out);
		min-width: 3px;
	}

	.bar-value {
		width: 60px;
		flex-shrink: 0;
		text-align: right;
		font-size: 0.78rem;
		color: var(--text-tertiary);
	}

	.bar-note {
		font-size: 0.75rem;
		color: var(--text-tertiary);
		font-style: italic;
		margin-top: var(--space-sm);
	}
</style>
