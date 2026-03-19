<script>
	/**
	 * HurdleExplainer — Visual explanation of the Double Hurdle model.
	 * Uses a funnel/pipeline metaphor to show how the two stages work.
	 * Designed for a non-technical audience.
	 */
	let { model } = $props();

	const pop = model?.population ?? {};
</script>

<div class="hurdle-explainer">
	<!-- Pipeline visualization -->
	<div class="pipeline">
		<!-- Stage 0: All users -->
		<div class="stage stage-0">
			<div class="stage-icon">👥</div>
			<div class="stage-content">
				<div class="stage-count mono">{pop.total_usagers?.toLocaleString('fr-FR') ?? '2 493'}</div>
				<div class="stage-label">usagers accidentés</div>
			</div>
		</div>

		<!-- Arrow 1 -->
		<div class="pipeline-arrow">
			<div class="arrow-line"></div>
			<div class="arrow-label">
				<span class="arrow-question">Qui sera gravement blessé ?</span>
			</div>
		</div>

		<!-- Stage 1: Hurdle 1 -->
		<div class="stage stage-h1">
			<div class="stage-badge badge-warn">Hurdle 1</div>
			<div class="stage-icon">🏥</div>
			<div class="stage-content">
				<div class="stage-count mono" style="color: var(--warn);">{pop.graves_h1 ?? 425}</div>
				<div class="stage-label">cas graves ({pop.pct_graves ?? 17}%)</div>
				<div class="stage-detail">Hospitalisés + tués</div>
			</div>
			<div class="stage-model">
				<span class="mono" style="font-size: 0.72rem;">AUC = 0,825</span>
				<span style="font-size: 0.72rem; color: var(--text-tertiary);">43 variables</span>
			</div>
		</div>

		<!-- Arrow 2 -->
		<div class="pipeline-arrow">
			<div class="arrow-line"></div>
			<div class="arrow-label">
				<span class="arrow-question">Parmi les graves, qui décédera ?</span>
			</div>
		</div>

		<!-- Stage 2: Hurdle 2 -->
		<div class="stage stage-h2">
			<div class="stage-badge badge-danger">Hurdle 2</div>
			<div class="stage-icon">⚠️</div>
			<div class="stage-content">
				<div class="stage-count mono" style="color: var(--danger);">{pop.tues_h2 ?? 43}</div>
				<div class="stage-label">décès ({pop.pct_tues_parmi_graves ?? 10.1}% des graves)</div>
			</div>
			<div class="stage-model">
				<span class="mono" style="font-size: 0.72rem;">AUC = 0,809</span>
				<span style="font-size: 0.72rem; color: var(--text-tertiary);">4 variables</span>
			</div>
		</div>
	</div>

	<!-- Key insight callout -->
	<div class="insight info-box" style="margin-top: var(--space-xl);">
		<strong>Pourquoi deux étapes ?</strong>
		Les facteurs qui provoquent un accident grave ne sont pas les mêmes que ceux qui
		déterminent si l'on y survit. Par exemple, rouler en moto augmente le risque d'être
		gravement blessé (Hurdle 1), mais une fois blessé grave, c'est l'âge, le port du casque
		et l'heure qui déterminent le pronostic vital (Hurdle 2).
	</div>
</div>

<style>
	.hurdle-explainer {
		max-width: 100%;
	}

	.pipeline {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0;
	}

	.stage {
		background: var(--surface);
		border: 1px solid var(--border);
		border-radius: var(--radius-lg);
		padding: var(--space-lg) var(--space-xl);
		text-align: center;
		position: relative;
		width: 100%;
		max-width: 380px;
		box-shadow: var(--shadow-sm);
	}

	.stage-h1 {
		border-color: var(--warn);
		border-width: 2px;
	}

	.stage-h2 {
		border-color: var(--danger);
		border-width: 2px;
	}

	.stage-badge {
		position: absolute;
		top: -10px;
		left: 50%;
		transform: translateX(-50%);
		font-family: var(--font-mono);
		font-size: 0.68rem;
		font-weight: 700;
		padding: 3px 12px;
		border-radius: 20px;
		letter-spacing: 0.05em;
	}

	.stage-icon {
		font-size: 1.8rem;
		margin-bottom: 6px;
	}

	.stage-count {
		font-size: 2rem;
		font-weight: 700;
		line-height: 1;
	}

	.stage-label {
		font-size: 0.92rem;
		font-weight: 500;
		color: var(--text-secondary);
		margin-top: 4px;
	}

	.stage-detail {
		font-size: 0.78rem;
		color: var(--text-tertiary);
		margin-top: 2px;
	}

	.stage-model {
		display: flex;
		justify-content: center;
		gap: var(--space-md);
		margin-top: var(--space-sm);
		padding-top: var(--space-sm);
		border-top: 1px solid var(--border-light);
	}

	/* Pipeline arrows */
	.pipeline-arrow {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: var(--space-md) 0;
	}

	.arrow-line {
		width: 2px;
		height: 28px;
		background: var(--border);
		position: relative;
	}

	.arrow-line::after {
		content: '▼';
		position: absolute;
		bottom: -10px;
		left: 50%;
		transform: translateX(-50%);
		font-size: 0.6rem;
		color: var(--text-tertiary);
	}

	.arrow-label {
		margin-top: 8px;
	}

	.arrow-question {
		font-size: 0.85rem;
		font-weight: 600;
		color: var(--accent);
		font-style: italic;
	}

	@media (max-width: 640px) {
		.stage {
			padding: var(--space-md);
		}
		.stage-count {
			font-size: 1.6rem;
		}
	}
</style>
