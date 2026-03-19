<script>
	import { onMount } from 'svelte';

	import accidentsData from '$lib/data/accidents.json';
	import summariesData from '$lib/data/summaries.json';
	import modelData from '$lib/data/model-results.json';

	import Hero from '$lib/components/Hero.svelte';
	import StatGrid from '$lib/components/StatGrid.svelte';
	import AccidentMap from '$lib/components/AccidentMap.svelte';
	import GravityBreakdown from '$lib/components/GravityBreakdown.svelte';
	import BarChart from '$lib/components/BarChart.svelte';
	import HourlyChart from '$lib/components/HourlyChart.svelte';
	import RiskFactors from '$lib/components/RiskFactors.svelte';
	import HurdleExplainer from '$lib/components/HurdleExplainer.svelte';
	import ForestPlot from '$lib/components/ForestPlot.svelte';
	import RiskCalculator from '$lib/components/RiskCalculator.svelte';
	import ProfileCards from '$lib/components/ProfileCards.svelte';

	import { fmt, pct, severityColor, VEHICLE_ICONS } from '$lib/utils/format.js';

	onMount(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				for (const entry of entries) {
					if (entry.isIntersecting) {
						entry.target.classList.add('visible');
					}
				}
			},
			{ threshold: 0.1, rootMargin: '0px 0px -60px 0px' }
		);

		document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

		function handleScroll() {
			const scrollY = window.scrollY;
			document.querySelectorAll('[data-parallax]').forEach((el) => {
				const speed = parseFloat(el.dataset.parallax) || 0.15;
				const rect = el.getBoundingClientRect();
				const center = rect.top + rect.height / 2;
				const offset = (center - window.innerHeight / 2) * speed;
				el.style.transform = `translateY(${offset}px)`;
			});
		}

		window.addEventListener('scroll', handleScroll, { passive: true });
		handleScroll();

		return () => {
			observer.disconnect();
			window.removeEventListener('scroll', handleScroll);
		};
	});

	let vehicleChartData = $derived(
		(summariesData.by_vehicle ?? []).map(d => ({
			label: (VEHICLE_ICONS[d.type_vehicule] || '') + ' ' + d.type_vehicule,
			value: d.total,
			rate: d.taux_grav,
		}))
	);

	let ageChartData = $derived(
		(summariesData.by_age ?? []).map(d => ({
			label: d.age_groupe,
			value: d.total,
			rate: d.taux_grav,
		}))
	);
</script>

<svelte:head>
	<title>Sécurité routière — La Réunion 2024</title>
</svelte:head>

<Hero summaries={summariesData} />


<section class="section" id="carte">
	<div class="container">
		<div class="reveal">
			<p class="section-label" data-parallax="0.04">01 · Cartographie</p>
			<h2 class="section-title" data-parallax="0.06">Où se produisent les accidents ?</h2>
			<p class="section-intro">
				Chaque point représente un accident corporel enregistré en 2024 à La Réunion.
				La couleur indique la gravité maximale parmi les usagers impliqués.
				Les accidents mortels sont affichés au premier plan.
			</p>
		</div>

		<div class="reveal">
			<AccidentMap accidents={accidentsData} />
		</div>

		<div class="reveal" style="margin-top: var(--space-xl);">
			<div class="info-box">
				<strong>934 accidents corporels</strong> ont été géolocalisés sur le département 974.
				Les zones les plus touchées sont les axes littoraux (RN1, RN2) et les centres urbains
				de Saint-Denis, Saint-Pierre et Saint-Paul.
			</div>
		</div>
	</div>
</section>


<section class="section" id="profils">
	<div class="container">
		<div class="reveal">
			<p class="section-label">02 · Profils des usagers</p>
			<h2 class="section-title">Qui est touché, et comment ?</h2>
			<p class="section-intro">
				Sur {fmt(summariesData.total_usagers)} usagers impliqués dans un accident,
				{summariesData.gravity_distribution?.pct_grave}% sont des cas graves
				(hospitalisés ou décédés). Voici comment ils se répartissent.
			</p>
		</div>

		<div class="reveal">
			<div class="card" style="padding: var(--space-xl);">
				<h3 style="margin-bottom: var(--space-lg); font-size: 1.1rem;">
					Chaque carré = 1% des usagers
				</h3>
				<GravityBreakdown distribution={summariesData.gravity_distribution} />
			</div>
		</div>

		<div class="reveal chart-row" style="margin-top: var(--space-xl);">
			<BarChart
				title="Par type de véhicule"
				items={vehicleChartData}
				showRate={true}
				colorFn={(item) => severityColor(item.rate / 100)}
				maxItems={8}
				note="% d'usagers gravement blessés par catégorie de véhicule"
			/>

			<BarChart
				title="Par tranche d'âge"
				items={ageChartData}
				showRate={true}
				colorFn={(item) => severityColor(item.rate / 100)}
				note="% d'usagers gravement blessés par groupe d'âge"
			/>
		</div>

		<div class="reveal" style="margin-top: var(--space-md);">
			<HourlyChart hourlyData={summariesData.hourly ?? []} />
		</div>

		<div class="reveal" style="margin-top: var(--space-md);">
			<div class="info-box">
				<strong>Le paradoxe horaire :</strong> la majorité des accidents se produisent
				en journée (heures de pointe), mais les accidents les plus graves surviennent
				la nuit — quand le trafic est réduit mais les vitesses plus élevées.
			</div>
		</div>
	</div>
</section>


<section class="section" id="facteurs">
	<div class="container">
		<div class="reveal">
			<p class="section-label">03 · Facteurs de risque</p>
			<h2 class="section-title">Quels facteurs augmentent la gravité ?</h2>
			<p class="section-intro">
				Avant de modéliser, comparons les taux de gravité selon les principales
				circonstances. Les écarts sont déjà visibles dans les données brutes.
			</p>
		</div>

		<div class="reveal">
			<RiskFactors summaries={summariesData} />
		</div>

		<div class="reveal" style="margin-top: var(--space-xl);">
			<div class="method-box">
				<strong style="color: var(--purple);">📐 Note méthodologique</strong> —
				Ces taux bruts sont descriptifs et ne tiennent pas compte des corrélations
				entre facteurs. Par exemple, les accidents de nuit surviennent souvent hors
				agglomération et impliquent des deux-roues — les effets se cumulent.
				Le modèle statistique (section suivante) isole chaque effet individuellement.
			</div>
		</div>
	</div>
</section>


<section class="section" id="modele">
	<div class="container">
		<div class="reveal">
			<p class="section-label" data-parallax="0.04">04 · Modélisation actuarielle</p>
			<h2 class="section-title" data-parallax="0.06">Le modèle Double Hurdle</h2>
			<p class="section-intro">
				Pour comprendre ce qui rend un accident grave — et ce qui détermine
				la survie — nous utilisons un modèle statistique en deux étapes.
			</p>
		</div>

		<div class="reveal">
			<HurdleExplainer model={modelData} />
		</div>

		<div class="reveal" style="margin-top: var(--space-2xl);">
			<h3 style="margin-bottom: var(--space-md);">
				Qu'est-ce qui aggrave un accident ?
			</h3>
			<p style="color: var(--text-secondary); margin-bottom: var(--space-lg); max-width: 60ch;">
				Explorez les résultats du modèle. Cliquez sur chaque facteur pour
				comprendre son effet. Basculez entre les deux étapes du modèle.
			</p>

			<ForestPlot
				h2OddsRatios={modelData.hurdle2?.odds_ratios ?? []}
				h1TopFactors={[...(modelData.hurdle1?.top_aggravating ?? []), ...(modelData.hurdle1?.top_protective ?? [])]}
			/>
		</div>

		<div class="reveal" style="margin-top: var(--space-xl);">
			<StatGrid stats={[
				{
					value: '0,825',
					label: 'AUC-ROC Hurdle 1',
					color: 'var(--accent)',
				},
				{
					value: '0,809',
					label: 'AUC-ROC Hurdle 2',
					color: 'var(--accent)',
				},
				{
					value: '0,597',
					label: 'Gini (H1)',
					color: 'var(--blue)',
				},
				{
					value: '4',
					label: 'Variables (H2)',
					color: 'var(--purple)',
				},
			]} />
		</div>

		<div class="reveal" style="margin-top: var(--space-lg);">
			<div class="method-box">
				<strong style="color: var(--purple);">🔬 Validation du modèle</strong> —
				Le test de Brant montre que 49% des variables violent l'hypothèse de cotes
				proportionnelles — justifiant le choix du Double Hurdle plutôt qu'un modèle
				ordinal unique. Les rankings des facteurs entre H1 et H2 divergent
				significativement (Spearman p &gt; 0.05), confirmant que les deux étapes
				captent des mécanismes distincts.
			</div>
		</div>
	</div>
</section>


<section class="section" id="risque">
	<div class="container">
		<div class="reveal">
			<p class="section-label" data-parallax="0.04">05 · Score de risque</p>
			<h2 class="section-title" data-parallax="0.06">Quel est votre niveau de risque ?</h2>
			<p class="section-intro">
				Le modèle permet de calculer un score de risque relatif en combinant
				les facteurs identifiés. L'écart entre le profil le plus sûr et le plus
				dangereux est de <strong class="mono">16×</strong>.
			</p>
		</div>

		<div class="reveal">
			<RiskCalculator model={modelData} />
		</div>

		<div class="reveal" style="margin-top: var(--space-xl);">
			<h3 style="margin-bottom: var(--space-lg);">Profils-types</h3>
			<ProfileCards />
		</div>
	</div>
</section>


<section class="section" id="conclusions">
	<div class="container">
		<div class="reveal">
			<p class="section-label">06 · Conclusions</p>
			<h2 class="section-title">Ce que nous apprend cette étude</h2>
		</div>

		<div class="reveal takeaways">
			<div class="takeaway card">
				<span class="takeaway-icon">🌙</span>
				<div>
					<h4>La nuit est le facteur le plus meurtrier</h4>
					<p>Un accident grave de nuit quadruple le risque de décès (OR ≈ 3,75).
					La combinaison vitesse + délais de secours rend la nuit particulièrement dangereuse.</p>
				</div>
			</div>

			<div class="takeaway card">
				<span class="takeaway-icon">🦺</span>
				<div>
					<h4>L'équipement sauve des vies</h4>
					<p>Porter un casque ou une ceinture divise le risque de décès par 4 en cas
					d'accident grave. C'est le facteur protecteur le plus puissant du modèle.</p>
				</div>
			</div>

			<div class="takeaway card">
				<span class="takeaway-icon">🏘️</span>
				<div>
					<h4>La ville protège</h4>
					<p>En agglomération, le risque de décès est divisé par 4 — effet combiné des
					vitesses réduites et de la proximité des services d'urgence.</p>
				</div>
			</div>

			<div class="takeaway card">
				<span class="takeaway-icon">📊</span>
				<div>
					<h4>Fréquence ≠ gravité</h4>
					<p>Les facteurs qui provoquent des accidents (Hurdle 1) ne sont pas les mêmes
					que ceux qui tuent (Hurdle 2). Cette distinction est essentielle pour cibler les
					actions de prévention.</p>
				</div>
			</div>
		</div>

		<div class="reveal" style="margin-top: var(--space-xl);">
			<div class="method-box">
				<strong style="color: var(--purple);">⚠️ Limites de l'étude</strong>
				<p style="margin-top: 8px;">
					Le Hurdle 2 repose sur seulement 43 décès, ce qui limite la puissance statistique
					(intervalles de confiance larges). La vitesse et l'alcoolémie — facteurs majeurs
					de gravité — ne figurent pas dans le BAAC simplifié. Les résultats sont spécifiques
					à La Réunion (réseau routier, climat tropical, accès aux secours) et leur
					transposition à d'autres territoires nécessiterait un recalibrage.
				</p>
			</div>
		</div>
	</div>
</section>


<footer class="site-footer">
	<div class="container">
		<div class="footer-content">
			<div class="footer-left">
				<p class="footer-title">Sécurité routière · La Réunion 2024</p>
				<p class="footer-subtitle">
					Étude actuarielle — Modèle Double Hurdle sur les données BAAC
				</p>
			</div>
			<div class="footer-right">
				<p class="footer-sources">
					<strong>Sources des données :</strong><br />
					BAAC 2024 — ONISR / data.gouv.fr<br />
					Météo France — données horaires dept. 974
				</p>
			</div>
		</div>
		<div class="footer-bottom">
			<p>Réalisé avec Svelte, Leaflet & D3 · Données publiques</p>
		</div>
	</div>
</footer>


<nav class="top-nav">
	<div class="nav-inner">
		<a href="#hero" class="nav-brand">🏝️ La Réunion 2024</a>
		<div class="nav-links">
			<a href="#carte">Carte</a>
			<a href="#profils">Profils</a>
			<a href="#facteurs">Facteurs</a>
			<a href="#modele">Modèle</a>
			<a href="#risque">Risque</a>
			<a href="#conclusions">Conclusions</a>
		</div>
	</div>
</nav>


<style>
	.chart-row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--space-md);
	}

	@media (max-width: 768px) {
		.chart-row {
			grid-template-columns: 1fr;
		}
	}

	.takeaways {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: var(--space-md);
	}

	.takeaway {
		display: flex;
		gap: var(--space-md);
		padding: var(--space-lg);
	}

	.takeaway-icon {
		font-size: 1.5rem;
		flex-shrink: 0;
	}

	.takeaway h4 {
		font-size: 1rem;
		font-weight: 700;
		margin-bottom: 6px;
	}

	.takeaway p {
		font-size: 0.88rem;
		color: var(--text-secondary);
		line-height: 1.6;
	}

	@media (max-width: 768px) {
		.takeaways {
			grid-template-columns: 1fr;
		}
	}

	.top-nav {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		z-index: 9000;
		background: rgba(250, 250, 247, 0.88);
		backdrop-filter: blur(12px);
		border-bottom: 1px solid var(--border-light);
	}

	.nav-inner {
		max-width: var(--max-width);
		margin: 0 auto;
		padding: 0 var(--space-lg);
		height: 48px;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.nav-brand {
		font-family: var(--font-display);
		font-weight: 700;
		font-size: 0.92rem;
		color: var(--text);
		text-decoration: none;
	}

	.nav-links {
		display: flex;
		gap: var(--space-lg);
	}

	.nav-links a {
		font-size: 0.78rem;
		font-weight: 500;
		color: var(--text-tertiary);
		text-decoration: none;
		transition: color 0.15s;
		letter-spacing: 0.02em;
	}

	.nav-links a:hover {
		color: var(--accent);
	}

	@media (max-width: 768px) {
		.nav-links {
			display: none;
		}
	}

	.site-footer {
		background: var(--text);
		color: var(--text-inverse);
		padding: var(--space-2xl) 0 var(--space-lg);
		margin-top: var(--space-2xl);
	}

	.footer-content {
		display: flex;
		justify-content: space-between;
		gap: var(--space-xl);
		margin-bottom: var(--space-xl);
	}

	.footer-title {
		font-family: var(--font-display);
		font-size: 1.1rem;
		font-weight: 700;
		margin-bottom: 4px;
	}

	.footer-subtitle {
		font-size: 0.85rem;
		opacity: 0.6;
	}

	.footer-sources {
		font-size: 0.82rem;
		opacity: 0.6;
		line-height: 1.7;
	}

	.footer-sources strong {
		opacity: 1;
	}

	.footer-bottom {
		border-top: 1px solid rgba(255,255,255,0.1);
		padding-top: var(--space-md);
		font-size: 0.75rem;
		opacity: 0.4;
	}

	@media (max-width: 640px) {
		.footer-content {
			flex-direction: column;
		}
	}
</style>
