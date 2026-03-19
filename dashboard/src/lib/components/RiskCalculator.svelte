<script>
	/**
	 * RiskCalculator — Interactive "what's my risk?" tool.
	 * Users select factors and see how their risk compares.
	 * Simplified version using the H2 odds ratios to communicate relative risk.
	 */
	let { model } = $props();

	/* User-selected profile */
	let isNight = $state(false);
	let isUrban = $state(true);
	let hasProtection = $state(true);
	let age = $state(30);

	/* Compute relative risk using H2 OR */
	let riskScore = $derived.by(() => {
		let score = 1;

		/* Night: OR = 3.75 */
		if (isNight) score *= 3.75;

		/* Urban (protective): OR = 0.25 → hors agglo = 1/0.25 = 4× */
		if (!isUrban) score *= (1 / 0.25);

		/* Protection (protective): OR = 0.26 → sans protection = 1/0.26 ≈ 3.85× */
		if (!hasProtection) score *= (1 / 0.26);

		/* Age: OR = 1.05 per year, reference = 30 */
		score *= Math.pow(1.05, age - 30);

		return score;
	});

	/* Reference: baseline risk (30 ans, jour, urbain, protégé) = 1.0 */
	let riskLabel = $derived(
		riskScore < 1.5 ? 'Faible' :
		riskScore < 4 ? 'Modéré' :
		riskScore < 10 ? 'Élevé' :
		'Très élevé'
	);

	let riskColor = $derived(
		riskScore < 1.5 ? 'var(--safe)' :
		riskScore < 4 ? 'var(--warn)' :
		'var(--danger)'
	);

	/* Gauge: log scale, capped display */
	let gaugeWidth = $derived(
		Math.min(100, (Math.log(riskScore + 1) / Math.log(60)) * 100)
	);
</script>

<div class="risk-calc card">
	<h4 class="calc-title">Calculateur de risque</h4>
	<p class="calc-subtitle">
		Sélectionnez un profil pour voir le risque relatif de décès en cas d'accident grave.
	</p>

	<div class="calc-grid">
		<!-- Controls -->
		<div class="controls">
			<label class="control">
				<span class="control-label">Moment</span>
				<div class="toggle-group">
					<button
						class="toggle-btn"
						class:active={!isNight}
						onclick={() => isNight = false}
					>☀️ Jour</button>
					<button
						class="toggle-btn"
						class:active={isNight}
						onclick={() => isNight = true}
					>🌙 Nuit</button>
				</div>
			</label>

			<label class="control">
				<span class="control-label">Lieu</span>
				<div class="toggle-group">
					<button
						class="toggle-btn"
						class:active={isUrban}
						onclick={() => isUrban = true}
					>🏘️ En ville</button>
					<button
						class="toggle-btn"
						class:active={!isUrban}
						onclick={() => isUrban = false}
					>🛣️ Hors agglo</button>
				</div>
			</label>

			<label class="control">
				<span class="control-label">Équipement</span>
				<div class="toggle-group">
					<button
						class="toggle-btn"
						class:active={hasProtection}
						onclick={() => hasProtection = true}
					>🦺 Protégé</button>
					<button
						class="toggle-btn"
						class:active={!hasProtection}
						onclick={() => hasProtection = false}
					>❌ Non protégé</button>
				</div>
			</label>

			<label class="control">
				<span class="control-label">Âge : <strong class="mono">{age} ans</strong></span>
				<input
					type="range"
					min="16"
					max="85"
					bind:value={age}
					class="age-slider"
				/>
				<div class="slider-labels">
					<span>16</span>
					<span>85</span>
				</div>
			</label>
		</div>

		<!-- Result display -->
		<div class="result">
			<div class="risk-gauge">
				<div class="gauge-track">
					<div
						class="gauge-fill"
						style="width: {gaugeWidth}%; background: {riskColor};"
					></div>
				</div>
				<div class="gauge-labels">
					<span>1×</span>
					<span>60×</span>
				</div>
			</div>

			<div class="risk-display">
				<span class="risk-multiplier mono" style="color: {riskColor};">
					{riskScore.toFixed(1)}×
				</span>
				<span class="risk-badge" style="background: {riskColor}; color: white;">
					{riskLabel}
				</span>
			</div>

			<p class="risk-explanation">
				{#if riskScore < 1.5}
					Ce profil a un risque proche du minimum — les conditions sont favorables à la survie.
				{:else if riskScore < 4}
					Le risque est modérément élevé. Un ou deux facteurs aggravants sont présents.
				{:else if riskScore < 10}
					Le risque de décès est significativement plus élevé que le profil de référence.
				{:else}
					Ce profil cumule plusieurs facteurs de risque majeurs.
					Le risque de décès est <strong>{riskScore.toFixed(0)} fois</strong> plus élevé
					que celui d'un conducteur protégé de 30 ans, en ville, de jour.
				{/if}
			</p>

			<p class="risk-ref-note">
				Référence : conducteur de 30 ans, de jour, en agglomération, avec ceinture/casque = 1,0×
			</p>
		</div>
	</div>
</div>

<style>
	.risk-calc {
		padding: var(--space-lg);
	}

	.calc-title {
		font-family: var(--font-body);
		font-size: 0.82rem;
		font-weight: 600;
		color: var(--text-secondary);
		text-transform: uppercase;
		letter-spacing: 0.04em;
		margin-bottom: 4px;
	}

	.calc-subtitle {
		font-size: 0.85rem;
		color: var(--text-tertiary);
		margin-bottom: var(--space-lg);
	}

	.calc-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--space-xl);
	}

	.controls {
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
	}

	.control {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	.control-label {
		font-size: 0.82rem;
		font-weight: 500;
		color: var(--text-secondary);
	}

	.toggle-group {
		display: flex;
		gap: 4px;
	}

	.toggle-btn {
		flex: 1;
		padding: 8px 12px;
		border: 1px solid var(--border);
		border-radius: var(--radius-sm);
		background: var(--surface);
		font-family: var(--font-body);
		font-size: 0.82rem;
		cursor: pointer;
		transition: all 0.15s;
		color: var(--text-secondary);
	}

	.toggle-btn:hover {
		border-color: var(--accent);
	}

	.toggle-btn.active {
		background: var(--accent-bg);
		border-color: var(--accent);
		color: var(--accent);
		font-weight: 600;
	}

	.age-slider {
		width: 100%;
		accent-color: var(--accent);
		cursor: pointer;
	}

	.slider-labels {
		display: flex;
		justify-content: space-between;
		font-size: 0.68rem;
		font-family: var(--font-mono);
		color: var(--text-tertiary);
	}

	/* Result */
	.result {
		display: flex;
		flex-direction: column;
		justify-content: center;
	}

	.risk-gauge {
		margin-bottom: var(--space-md);
	}

	.gauge-track {
		height: 12px;
		background: var(--surface-alt);
		border-radius: 6px;
		overflow: hidden;
	}

	.gauge-fill {
		height: 100%;
		border-radius: 6px;
		transition: width 0.5s var(--ease-out), background 0.3s;
	}

	.gauge-labels {
		display: flex;
		justify-content: space-between;
		font-family: var(--font-mono);
		font-size: 0.65rem;
		color: var(--text-tertiary);
		margin-top: 2px;
	}

	.risk-display {
		display: flex;
		align-items: center;
		gap: var(--space-md);
		margin-bottom: var(--space-md);
	}

	.risk-multiplier {
		font-size: 2.8rem;
		font-weight: 700;
		line-height: 1;
		transition: color 0.3s;
	}

	.risk-badge {
		font-family: var(--font-mono);
		font-size: 0.72rem;
		font-weight: 700;
		padding: 4px 12px;
		border-radius: 20px;
		letter-spacing: 0.05em;
		text-transform: uppercase;
	}

	.risk-explanation {
		font-size: 0.88rem;
		color: var(--text-secondary);
		line-height: 1.6;
	}

	.risk-ref-note {
		font-size: 0.72rem;
		color: var(--text-tertiary);
		font-style: italic;
		margin-top: var(--space-sm);
	}

	@media (max-width: 768px) {
		.calc-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
