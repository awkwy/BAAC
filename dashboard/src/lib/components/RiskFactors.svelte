<script>
	/**
	 * RiskFactors — Side-by-side comparison of severity rates
	 * across different factor categories (night/day, urban/rural, etc.)
	 * This is what makes the story click for a non-technical audience.
	 */
	import { pct, severityColor } from '$lib/utils/format.js';

	let { summaries = {} } = $props();

	/* Build comparison pairs from summaries */
	let comparisons = $derived.by(() => {
		const pairs = [];

		/* Night vs Day */
		const night = summaries.night_vs_day?.find(d => d.nuit === 1);
		const day = summaries.night_vs_day?.find(d => d.nuit === 0);
		if (night && day) {
			pairs.push({
				title: 'Nuit vs Jour',
				a: { label: '🌙 Nuit', rate: night.taux_grav, count: night.graves, total: night.total },
				b: { label: '☀️ Jour', rate: day.taux_grav, count: day.graves, total: day.total },
			});
		}

		/* Rural vs Urban */
		const rural = summaries.agglo_vs_rural?.find(d => d.en_agglomeration === 0);
		const urban = summaries.agglo_vs_rural?.find(d => d.en_agglomeration === 1);
		if (rural && urban) {
			pairs.push({
				title: 'Hors agglo vs En agglo',
				a: { label: '🛣️ Hors agglo', rate: rural.taux_grav, count: rural.graves, total: rural.total },
				b: { label: '🏘️ En agglo', rate: urban.taux_grav, count: urban.graves, total: urban.total },
			});
		}

		/* By collision type */
		const frontal = summaries.by_collision?.find(d => d.type_collision === 'frontale');
		const side = summaries.by_collision?.find(d => d.type_collision === 'côté');
		if (frontal && side) {
			pairs.push({
				title: 'Type de collision',
				a: { label: '💥 Frontale', rate: frontal.taux_grav, count: frontal.graves, total: frontal.total },
				b: { label: '↗️ Côté', rate: side.taux_grav, count: side.graves, total: side.total },
			});
		}

		/* Weather */
		const rain = summaries.by_weather?.find(d => d.atm_groupe === 'pluie');
		const normal = summaries.by_weather?.find(d => d.atm_groupe === 'normale');
		if (rain && normal) {
			pairs.push({
				title: 'Conditions météo',
				a: { label: '🌧️ Pluie', rate: rain.taux_grav, count: rain.graves, total: rain.total },
				b: { label: '☀️ Normale', rate: normal.taux_grav, count: normal.graves, total: normal.total },
			});
		}

		return pairs;
	});
</script>

<div class="risk-factors">
	<div class="factor-grid">
		{#each comparisons as pair}
			<div class="factor-card card">
				<h4 class="factor-title">{pair.title}</h4>
				<div class="factor-comparison">
					{#each [pair.a, pair.b] as side}
						<div class="factor-side">
							<span class="factor-label">{side.label}</span>
							<div class="factor-bar-track">
								<div
									class="factor-bar-fill"
									style="width: {Math.min(side.rate, 100)}%; background: {severityColor(side.rate / 100)};"
								></div>
							</div>
							<div class="factor-stats">
								<span class="factor-rate mono" style="color: {severityColor(side.rate / 100)};">
									{side.rate}%
								</span>
								<span class="factor-count">{side.count}/{side.total}</span>
							</div>
						</div>
					{/each}
				</div>
			</div>
		{/each}
	</div>
</div>

<style>
	.factor-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: var(--space-md);
	}

	.factor-card {
		padding: var(--space-lg);
	}

	.factor-title {
		font-family: var(--font-body);
		font-size: 0.78rem;
		font-weight: 600;
		color: var(--text-secondary);
		text-transform: uppercase;
		letter-spacing: 0.04em;
		margin-bottom: var(--space-md);
	}

	.factor-comparison {
		display: flex;
		flex-direction: column;
		gap: var(--space-sm);
	}

	.factor-side {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.factor-label {
		font-size: 0.85rem;
		font-weight: 500;
	}

	.factor-bar-track {
		height: 10px;
		background: var(--surface-alt);
		border-radius: 5px;
		overflow: hidden;
	}

	.factor-bar-fill {
		height: 100%;
		border-radius: 5px;
		transition: width 0.6s var(--ease-out);
		min-width: 3px;
	}

	.factor-stats {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.factor-rate {
		font-size: 0.82rem;
		font-weight: 700;
	}

	.factor-count {
		font-size: 0.72rem;
		color: var(--text-tertiary);
		font-family: var(--font-mono);
	}

	@media (max-width: 640px) {
		.factor-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
