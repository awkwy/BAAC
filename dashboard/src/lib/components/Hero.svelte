<script>
	/**
	 * Hero section — editorial opening with key stats.
	 * Sets the tone: serious topic, clear data, bold typography.
	 */
	import { fmt } from '$lib/utils/format.js';

	let { summaries } = $props();

	const gd = summaries?.gravity_distribution ?? {};
	const pctGrave = ((gd.pct_grave ?? 16.7).toFixed(1)).replace('.', ',') + ' %';
</script>

<section class="hero" id="hero">
	<!-- Subtle topographic background texture — parallax layer -->
	<div class="hero-bg" data-parallax="-0.2"></div>

	<div class="hero-content container">
		<p class="hero-eyebrow" data-parallax="0.05">Étude actuarielle · La Réunion · 2024</p>

		<h1 class="hero-title">
			Comprendre les <em>risques</em><br />sur les routes réunionnaises
		</h1>

		<p class="hero-subtitle">
			En 2024, <strong>{fmt(summaries?.total_accidents ?? 934)} accidents corporels</strong>
			ont été enregistrés à La Réunion, impliquant
			<strong>{fmt(summaries?.total_usagers ?? 2565)} usagers</strong>.
			Cette étude analyse les facteurs qui rendent un accident <em>grave</em> — et ceux qui déterminent
			si un blessé grave survivra.
		</p>

		<!-- Key stat cards -->
		<div class="hero-stats">
			<div class="hero-stat">
				<span class="hero-stat-value mono">{fmt(summaries?.total_accidents ?? 934)}</span>
				<span class="hero-stat-label">Accidents corporels</span>
			</div>
			<div class="hero-stat-divider"></div>
			<div class="hero-stat">
				<span class="hero-stat-value mono" style="color: var(--danger)">{gd.tue ?? 43}</span>
				<span class="hero-stat-label">Tués</span>
			</div>
			<div class="hero-stat-divider"></div>
			<div class="hero-stat">
				<span class="hero-stat-value mono" style="color: var(--warn)">{gd.hospitalise ?? 386}</span>
				<span class="hero-stat-label">Hospitalisés</span>
			</div>
			<div class="hero-stat-divider"></div>
			<div class="hero-stat">
				<span class="hero-stat-value mono" style="color: var(--accent)">{pctGrave}</span>
				<span class="hero-stat-label">Taux de gravité</span>
			</div>
		</div>

		<div class="hero-scroll-hint">
			<span>Défiler pour explorer</span>
			<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
				<path d="M10 4v12M5 11l5 5 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
			</svg>
		</div>
	</div>
</section>

<style>
	.hero {
		position: relative;
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
		padding: var(--space-2xl) 0;
	}

	.hero-bg {
		position: absolute;
		inset: 0;
		background:
			radial-gradient(ellipse 80% 60% at 50% 0%, rgba(212, 118, 10, 0.06) 0%, transparent 70%),
			linear-gradient(180deg, var(--bg-warm) 0%, var(--bg) 100%);
		z-index: 0;
	}

	.hero-content {
		position: relative;
		z-index: 1;
		text-align: center;
		max-width: 800px;
	}

	.hero-eyebrow {
		font-family: var(--font-mono);
		font-size: 0.72rem;
		font-weight: 600;
		letter-spacing: 0.14em;
		text-transform: uppercase;
		color: var(--accent);
		margin-bottom: var(--space-lg);
	}

	.hero-title {
		font-size: clamp(2.4rem, 6vw, 3.8rem);
		font-weight: 800;
		line-height: 1.1;
		margin-bottom: var(--space-lg);
		letter-spacing: -0.025em;
	}

	.hero-title em {
		font-style: italic;
		color: var(--danger);
	}

	.hero-subtitle {
		font-size: 1.15rem;
		line-height: 1.7;
		color: var(--text-secondary);
		max-width: 56ch;
		margin: 0 auto var(--space-xl);
	}

	.hero-subtitle strong {
		color: var(--text);
		font-weight: 600;
	}

	.hero-subtitle em {
		color: var(--danger);
		font-style: normal;
		font-weight: 600;
	}

	.hero-stats {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--space-xl);
		margin-top: var(--space-xl);
		flex-wrap: wrap;
	}

	.hero-stat {
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.hero-stat-value {
		font-size: 2.6rem;
		font-weight: 700;
		line-height: 1;
	}

	.hero-stat-label {
		font-size: 0.75rem;
		font-weight: 500;
		color: var(--text-tertiary);
		text-transform: uppercase;
		letter-spacing: 0.08em;
		margin-top: 6px;
	}

	.hero-stat-divider {
		width: 1px;
		height: 40px;
		background: var(--border);
	}

	.hero-scroll-hint {
		margin-top: var(--space-3xl);
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 6px;
		color: var(--text-tertiary);
		font-size: 0.82rem;
		animation: float 2.5s ease-in-out infinite;
	}

	@keyframes float {
		0%, 100% { transform: translateY(0); }
		50% { transform: translateY(6px); }
	}

	@media (max-width: 640px) {
		.hero-stats { gap: var(--space-lg); }
		.hero-stat-divider { display: none; }
		.hero-stat-value { font-size: 2rem; }
	}
</style>
