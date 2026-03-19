<script>
	/**
	 * ForestPlot — Interactive visualization of the Double Hurdle model results.
	 * Redesigned for maximum accessibility to non-technical audiences:
	 *   - Click any row to lock its detail panel open
	 *   - Toggle between the two model stages (H1 = severity, H2 = fatality)
	 *   - Animated entry, colored bars, plain-language interpretations
	 *   - Hover shows the interpretation; click pins it
	 */
	import { sigStars } from '$lib/utils/format.js';

	let {
		h2OddsRatios = [],
		h1TopFactors = [],
	} = $props();

	/* Which model stage is visible */
	let activeTab = $state('h2');

	/* Hover & click states */
	let hoveredItem = $state(null);
	let selectedItem = $state(null);

	/* The active item to show detail for (click takes priority over hover) */
	let activeItem = $derived(selectedItem ?? hoveredItem);

	/* Current dataset based on tab */
	let currentData = $derived(activeTab === 'h2' ? h2OddsRatios : h1Display);

	/* Convert H1 top factors into a format matching H2 OR structure */
	let h1Display = $derived(
		[...h1TopFactors].map(d => ({
			...d,
			variable: d.feature,
			CI_lo: d.OR * 0.7,
			CI_hi: d.OR * 1.3,
			p: 0.01,
			interpretation: d.label + (d.OR > 1
				? ` multiplie le risque de blessure grave par ${d.OR.toFixed(1)}`
				: ` divise le risque de blessure grave par ${(1/d.OR).toFixed(1)}`),
		}))
	);

	/* Compute x-axis range to fit all CIs (log scale) */
	let xMin = $derived(Math.min(0.08, ...currentData.map(d => (d.CI_lo ?? d.OR * 0.7) * 0.7)));
	let xMax = $derived(Math.max(5, ...currentData.map(d => (d.CI_hi ?? d.OR * 1.3) * 1.3)));

	function xPos(or) {
		const logMin = Math.log(xMin);
		const logMax = Math.log(xMax);
		const logVal = Math.log(Math.max(or, 0.01));
		return ((logVal - logMin) / (logMax - logMin)) * 100;
	}

	let refLinePos = $derived(xPos(1));

	let sorted = $derived(
		[...currentData].sort((a, b) => a.OR - b.OR)
	);

	function handleRowClick(item) {
		selectedItem = selectedItem === item ? null : item;
	}
</script>

<div class="fp-wrapper">
	<!-- Tab bar: toggle between the two stages -->
	<div class="fp-tabs">
		<button
			class="fp-tab"
			class:active={activeTab === 'h2'}
			onclick={() => { activeTab = 'h2'; selectedItem = null; }}
		>
			<span class="tab-icon">⚠️</span>
			<span class="tab-text">
				<strong>Qu'est-ce qui tue ?</strong>
				<small>Facteurs de mortalité (Hurdle 2)</small>
			</span>
		</button>
		<button
			class="fp-tab"
			class:active={activeTab === 'h1'}
			onclick={() => { activeTab = 'h1'; selectedItem = null; }}
		>
			<span class="tab-icon">🏥</span>
			<span class="tab-text">
				<strong>Qu'est-ce qui blesse ?</strong>
				<small>Facteurs de gravité (Hurdle 1)</small>
			</span>
		</button>
	</div>

	<div class="fp-body card">
		<!-- Axis header -->
		<div class="fp-axis-header">
			<span class="fp-axis-left">← Protège</span>
			<span class="fp-axis-center mono">OR = 1</span>
			<span class="fp-axis-right">Aggrave →</span>
		</div>

		<!-- Chart rows -->
		<div class="fp-chart">
			<!-- Reference line at OR = 1 -->
			<div class="fp-refline" style="left: {refLinePos}%;"></div>

			{#each sorted as item, i}
				{@const isProtective = item.OR < 1}
				{@const color = isProtective ? 'var(--blue)' : 'var(--danger)'}
				{@const ciLeft = xPos(item.CI_lo ?? item.OR * 0.7)}
				{@const ciRight = xPos(item.CI_hi ?? item.OR * 1.3)}
				{@const pointPos = xPos(item.OR)}
				{@const isActive = activeItem === item}

				<button
					class="fp-row"
					class:active={isActive}
					class:selected={selectedItem === item}
					style="animation-delay: {i * 80}ms;"
					onmouseenter={() => hoveredItem = item}
					onmouseleave={() => hoveredItem = null}
					onclick={() => handleRowClick(item)}
				>
					<!-- Label column -->
					<div class="fp-label">
						<span class="fp-var-name">{item.label}</span>
						<span class="fp-or-badge mono" style="background: {isProtective ? 'var(--blue-bg)' : 'var(--danger-bg)'}; color: {color};">
							{item.OR < 1 ? '÷' : '×'}{item.OR < 1 ? (1/item.OR).toFixed(1) : item.OR.toFixed(1)}
						</span>
					</div>

					<!-- Bar area -->
					<div class="fp-bar-area">
						<!-- Confidence interval -->
						{#if item.CI_lo && item.CI_hi}
							<div
								class="fp-ci"
								style="left: {ciLeft}%; width: {ciRight - ciLeft}%; background: {color};"
							></div>
						{/if}
						<!-- Point estimate -->
						<div
							class="fp-point"
							style="left: {pointPos}%; background: {color};"
						></div>
						<!-- Animated bar from OR=1 to the point -->
						<div
							class="fp-bar-fill"
							style="
								left: {Math.min(refLinePos, pointPos)}%;
								width: {Math.abs(pointPos - refLinePos)}%;
								background: {color};
							"
						></div>
					</div>

					<!-- Significance -->
					<span class="fp-sig mono" style="color: {color};">
						{item.p != null ? sigStars(item.p) : ''}
					</span>
				</button>

				<!-- Detail panel (shown when active) -->
				{#if isActive && item.interpretation}
					<div class="fp-detail" style="border-left-color: {color};">
						<p class="fp-detail-text">💡 {item.interpretation}</p>
						{#if item.CI_lo && item.CI_hi}
							<p class="fp-detail-ci mono">
								OR = {item.OR.toFixed(2)} — IC 95% [{item.CI_lo.toFixed(2)} – {item.CI_hi.toFixed(2)}]
								{#if item.p != null}
									— p = {item.p < 0.001 ? '< 0,001' : item.p.toFixed(3).replace('.', ',')}
								{/if}
							</p>
						{/if}
					</div>
				{/if}
			{/each}
		</div>

		<!-- Guide -->
		<div class="fp-guide">
			<p>
				<strong>Comment lire ce graphique ?</strong>
				Chaque ligne représente un facteur. Un OR > 1 (à droite) signifie que ce
				facteur <em>augmente</em> le risque. Un OR &lt; 1 (à gauche) signifie
				qu'il le <em>réduit</em>. Cliquez sur une ligne pour voir les détails.
			</p>
		</div>
	</div>
</div>

<style>
	.fp-wrapper {
		display: flex;
		flex-direction: column;
		gap: 0;
	}

	/* ── Tabs ────────────────────────── */
	.fp-tabs {
		display: flex;
		gap: 4px;
	}

	.fp-tab {
		flex: 1;
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 14px 18px;
		border: 1px solid var(--border);
		border-bottom: none;
		border-radius: var(--radius-md) var(--radius-md) 0 0;
		background: var(--surface-alt);
		cursor: pointer;
		font-family: inherit;
		color: var(--text-secondary);
		transition: all 0.2s;
	}

	.fp-tab.active {
		background: var(--surface);
		color: var(--text);
		border-color: var(--border);
		box-shadow: 0 2px 0 var(--surface);
		position: relative;
		z-index: 1;
	}

	.tab-icon {
		font-size: 1.3rem;
	}

	.tab-text {
		display: flex;
		flex-direction: column;
		text-align: left;
	}

	.tab-text strong {
		font-size: 0.92rem;
	}

	.tab-text small {
		font-size: 0.72rem;
		color: var(--text-tertiary);
	}

	/* ── Body ────────────────────────── */
	.fp-body {
		border-radius: 0 0 var(--radius-md) var(--radius-md);
		border-top: 1px solid var(--border);
		padding: var(--space-lg);
	}

	.fp-axis-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding-bottom: var(--space-sm);
		border-bottom: 1px solid var(--border-light);
		margin-bottom: var(--space-md);
		font-size: 0.72rem;
		color: var(--text-tertiary);
	}

	.fp-axis-left { color: var(--blue); font-weight: 600; }
	.fp-axis-right { color: var(--danger); font-weight: 600; }
	.fp-axis-center { opacity: 0.5; }

	/* ── Chart ───────────────────────── */
	.fp-chart {
		position: relative;
	}

	.fp-refline {
		position: absolute;
		top: 0;
		bottom: 0;
		width: 1px;
		background: var(--text);
		opacity: 0.12;
		z-index: 0;
	}

	.fp-row {
		display: flex;
		align-items: center;
		gap: var(--space-md);
		padding: 10px 8px;
		border-radius: var(--radius-sm);
		border: 1px solid transparent;
		background: none;
		width: 100%;
		font-family: inherit;
		color: inherit;
		cursor: pointer;
		transition: all 0.2s var(--ease-out);
		opacity: 0;
		animation: rowSlideIn 0.4s var(--ease-out) forwards;
	}

	@keyframes rowSlideIn {
		from { opacity: 0; transform: translateX(-10px); }
		to { opacity: 1; transform: translateX(0); }
	}

	.fp-row:hover {
		background: var(--surface-alt);
		border-color: var(--border-light);
	}

	.fp-row.selected {
		background: var(--accent-bg);
		border-color: var(--accent);
	}

	.fp-label {
		width: 180px;
		flex-shrink: 0;
		display: flex;
		align-items: center;
		gap: 8px;
		text-align: left;
	}

	.fp-var-name {
		font-size: 0.88rem;
		font-weight: 500;
		color: var(--text);
		flex: 1;
	}

	.fp-or-badge {
		font-size: 0.72rem;
		font-weight: 700;
		padding: 2px 8px;
		border-radius: 12px;
		white-space: nowrap;
	}

	.fp-bar-area {
		flex: 1;
		position: relative;
		height: 28px;
	}

	.fp-bar-fill {
		position: absolute;
		top: 50%;
		transform: translateY(-50%);
		height: 10px;
		border-radius: 5px;
		opacity: 0.18;
		transition: all 0.4s var(--ease-out);
	}

	.fp-row:hover .fp-bar-fill,
	.fp-row.selected .fp-bar-fill {
		opacity: 0.35;
		height: 14px;
	}

	.fp-ci {
		position: absolute;
		top: 50%;
		transform: translateY(-50%);
		height: 3px;
		border-radius: 2px;
		opacity: 0.4;
	}

	.fp-point {
		position: absolute;
		top: 50%;
		transform: translate(-50%, -50%);
		width: 12px;
		height: 12px;
		border-radius: 50%;
		border: 2px solid white;
		z-index: 2;
		box-shadow: 0 1px 4px rgba(0,0,0,0.15);
		transition: transform 0.2s;
	}

	.fp-row:hover .fp-point {
		transform: translate(-50%, -50%) scale(1.3);
	}

	.fp-sig {
		width: 30px;
		flex-shrink: 0;
		text-align: center;
		font-size: 0.75rem;
		font-weight: 700;
	}

	/* ── Detail panel ────────────────── */
	.fp-detail {
		margin: -4px 0 8px 0;
		padding: 10px 16px;
		border-left: 3px solid;
		background: var(--surface-alt);
		border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
		animation: detailIn 0.25s var(--ease-out);
	}

	@keyframes detailIn {
		from { opacity: 0; transform: translateY(-6px); }
		to { opacity: 1; transform: translateY(0); }
	}

	.fp-detail-text {
		font-size: 0.88rem;
		color: var(--text);
		line-height: 1.5;
	}

	.fp-detail-ci {
		font-size: 0.72rem;
		color: var(--text-tertiary);
		margin-top: 4px;
	}

	/* ── Guide ───────────────────────── */
	.fp-guide {
		margin-top: var(--space-lg);
		padding-top: var(--space-md);
		border-top: 1px solid var(--border-light);
	}

	.fp-guide p {
		font-size: 0.82rem;
		color: var(--text-tertiary);
		line-height: 1.6;
		max-width: none;
	}

	.fp-guide strong {
		color: var(--text-secondary);
	}

	.fp-guide em {
		font-style: normal;
		font-weight: 600;
	}

	@media (max-width: 640px) {
		.fp-label { width: 120px; }
		.fp-tabs { flex-direction: column; }
		.fp-tab { border-radius: var(--radius-sm); border-bottom: 1px solid var(--border); }
	}
</style>
