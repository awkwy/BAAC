<script>
	/**
	 * StatGrid — a row of key statistics displayed in a grid.
	 * Used in the gravity breakdown section and elsewhere.
	 *
	 * Props:
	 *   stats: Array of { value, label, color? }
	 */
	let { stats = [] } = $props();
</script>

<div class="stat-grid" style="--cols: {stats.length}">
	{#each stats as stat}
		<div class="stat-card card">
			<span
				class="stat-value mono"
				style={stat.color ? `color: ${stat.color}` : ''}
			>
				{stat.value}
			</span>
			<span class="stat-label">{stat.label}</span>
		</div>
	{/each}
</div>

<style>
	.stat-grid {
		display: grid;
		grid-template-columns: repeat(var(--cols, 4), 1fr);
		gap: var(--space-md);
	}

	.stat-card {
		text-align: center;
		padding: var(--space-lg) var(--space-md);
	}

	@media (max-width: 640px) {
		.stat-grid {
			grid-template-columns: repeat(2, 1fr);
		}
	}
</style>
