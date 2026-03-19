<script>
	/**
	 * HourlyChart — vertical bar chart showing accident counts per hour.
	 * Each bar is colored by the proportion of severe accidents at that hour.
	 * Reveals the "hourly paradox": most accidents by day, most severe at night.
	 */
	import { severityColor } from '$lib/utils/format.js';

	let { hourlyData = [] } = $props();

	let maxCount = $derived(Math.max(...hourlyData.map(h => h.total), 1));

	let hoveredHour = $state(null);
</script>

<div class="hourly-chart card">
	<h4 class="chart-title">Répartition horaire des accidents</h4>
	<p class="chart-subtitle">
		Couleur = proportion d'accidents graves à cette heure
	</p>

	<div class="chart-area">
		<div class="bars">
			{#each hourlyData as h}
				{@const heightPct = (h.total / maxCount) * 100}
				{@const gravRate = h.total > 0 ? h.graves / h.total : 0}
				{@const color = severityColor(gravRate)}
				<div
					class="bar-col"
					onmouseenter={() => hoveredHour = h}
					onmouseleave={() => hoveredHour = null}
				>
					<div
						class="bar"
						style="height: {heightPct}%; background: {color};"
					></div>
				</div>
			{/each}
		</div>
		<div class="x-labels">
			<span>0h</span>
			<span>6h</span>
			<span>12h</span>
			<span>18h</span>
			<span>23h</span>
		</div>
	</div>

	<!-- Hover tooltip -->
	{#if hoveredHour}
		<div class="hover-info">
			<strong>{hoveredHour.heure}h</strong> — {hoveredHour.total} accidents
			({hoveredHour.graves} graves, {hoveredHour.tues} tués)
			<span class="mono" style="color: {severityColor(hoveredHour.taux_grav / 100)};">
				{hoveredHour.taux_grav}% graves
			</span>
		</div>
	{/if}

	<div class="chart-legend">
		<span class="legend-entry"><span class="dot" style="background: var(--safe);"></span> &lt; 18% graves</span>
		<span class="legend-entry"><span class="dot" style="background: var(--warn);"></span> 18–35% graves</span>
		<span class="legend-entry"><span class="dot" style="background: var(--danger);"></span> &gt; 35% graves</span>
	</div>
</div>

<style>
	.hourly-chart {
		padding: var(--space-lg);
	}

	.chart-title {
		font-family: var(--font-body);
		font-size: 0.82rem;
		font-weight: 600;
		color: var(--text-secondary);
		text-transform: uppercase;
		letter-spacing: 0.04em;
		margin-bottom: 2px;
	}

	.chart-subtitle {
		font-size: 0.75rem;
		color: var(--text-tertiary);
		margin-bottom: var(--space-md);
	}

	.chart-area {
		position: relative;
	}

	.bars {
		display: flex;
		align-items: flex-end;
		height: 140px;
		gap: 2px;
		padding-bottom: 2px;
	}

	.bar-col {
		flex: 1;
		height: 100%;
		display: flex;
		align-items: flex-end;
		cursor: pointer;
	}

	.bar {
		width: 100%;
		border-radius: 2px 2px 0 0;
		opacity: 0.75;
		transition: opacity 0.2s, height 0.6s var(--ease-out);
		min-height: 2px;
	}

	.bar-col:hover .bar {
		opacity: 1;
	}

	.x-labels {
		display: flex;
		justify-content: space-between;
		font-family: var(--font-mono);
		font-size: 0.68rem;
		color: var(--text-tertiary);
		margin-top: 4px;
	}

	.hover-info {
		margin-top: var(--space-sm);
		font-size: 0.82rem;
		color: var(--text-secondary);
		display: flex;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
	}

	.chart-legend {
		display: flex;
		gap: var(--space-md);
		margin-top: var(--space-sm);
		font-size: 0.72rem;
		color: var(--text-tertiary);
	}

	.legend-entry {
		display: flex;
		align-items: center;
		gap: 4px;
	}

	.dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
	}
</style>
