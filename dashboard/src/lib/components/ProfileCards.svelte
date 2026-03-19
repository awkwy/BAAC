<script>
	/**
	 * ProfileCards — risk archetype cards showing extreme profiles.
	 * Makes the model results tangible by showing real-world profiles.
	 */

	const profiles = [
		{
			title: 'Profil à risque maximal',
			icon: '🔴',
			borderColor: 'var(--danger)',
			bg: 'var(--danger-bg)',
			multiplier: '~57×',
			factors: [
				'Motard sans casque',
				'Nuit, hors agglomération',
				'65 ans et plus',
			],
			description: 'Ce profil cumule tous les facteurs aggravants identifiés par le modèle. Le risque de décès en cas d\'accident grave est considérablement élevé.',
		},
		{
			title: 'Profil à risque minimal',
			icon: '🟢',
			borderColor: 'var(--safe)',
			bg: 'var(--safe-bg)',
			multiplier: '1×',
			factors: [
				'Automobiliste avec ceinture',
				'Jour, en agglomération',
				'25–35 ans',
			],
			description: 'Le profil de référence du modèle. Conditions optimales de survie en cas d\'accident grave.',
		},
		{
			title: 'Profil paradoxal',
			icon: '🟡',
			borderColor: 'var(--warn)',
			bg: 'rgba(212, 150, 10, 0.06)',
			multiplier: '~4×',
			factors: [
				'Piéton en ville, de jour',
				'40 ans',
				'Accident fréquent, mais mortalité modérée',
			],
			description: 'Les piétons en zone urbaine ont un taux d\'accidents élevé mais bénéficient de la proximité des secours et des vitesses modérées.',
		},
	];
</script>

<div class="profile-grid">
	{#each profiles as profile}
		<div
			class="profile-card card"
			style="border-left: 4px solid {profile.borderColor};"
		>
			<div class="profile-header">
				<span class="profile-icon">{profile.icon}</span>
				<h4 class="profile-title">{profile.title}</h4>
			</div>

			<div class="profile-multiplier mono" style="color: {profile.borderColor};">
				{profile.multiplier}
			</div>

			<ul class="profile-factors">
				{#each profile.factors as factor}
					<li>{factor}</li>
				{/each}
			</ul>

			<p class="profile-desc">{profile.description}</p>
		</div>
	{/each}
</div>

<style>
	.profile-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: var(--space-md);
	}

	.profile-card {
		padding: var(--space-lg);
	}

	.profile-header {
		display: flex;
		align-items: center;
		gap: 8px;
		margin-bottom: var(--space-sm);
	}

	.profile-icon {
		font-size: 1.3rem;
	}

	.profile-title {
		font-size: 0.92rem;
		font-weight: 700;
	}

	.profile-multiplier {
		font-size: 2rem;
		font-weight: 700;
		line-height: 1;
		margin-bottom: var(--space-md);
	}

	.profile-factors {
		list-style: none;
		padding: 0;
		margin-bottom: var(--space-md);
	}

	.profile-factors li {
		font-size: 0.85rem;
		color: var(--text-secondary);
		padding: 4px 0;
		border-bottom: 1px solid var(--border-light);
	}

	.profile-factors li:last-child {
		border-bottom: none;
	}

	.profile-desc {
		font-size: 0.78rem;
		color: var(--text-tertiary);
		line-height: 1.6;
	}

	@media (max-width: 768px) {
		.profile-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
