# Accidentologie à La Réunion — 2024

**934 accidents corporels. 2 565 usagers impliqués. Quels facteurs déterminent la gravité ?**

Dashboard SvelteKit interactif pour explorer les accidents de la route à La Réunion (département 974), basé sur les données BAAC 2024.

> 🔗 **[Voir le dashboard en ligne](https://votre-user.github.io/securite-routiere-974/)**

---

## Résultats clés

### Qui est le plus à risque ?

| Profil | Taux de gravité | Facteur principal |
|--------|:-:|---|
| **Piétons** | 32 % | Vulnérabilité physique, médiane d'âge élevée (47 ans) |
| **2RM > 125 cm³** | ~25 % | Vitesse + exposition corporelle |
| **Conducteurs** | 17 % | Volume le plus élevé (1 500+ usagers) |
| **Passagers** | 13 % | Plus jeunes, mieux protégés |

### Ce que le modèle Double Hurdle révèle

| | Devenir un cas grave (H1) | Décéder parmi les graves (H2) |
|---|---|---|
| **n°1** | Collision frontale | Âge / vulnérabilité physique |
| **n°2** | Absence d'équipement | Type de choc |
| **n°3** | Route hors agglomération | Vitesse (type de route) |
| **n°4** | 2 roues motorisés | L'équipement ne suffit plus |
| **n°5** | Conditions nocturnes | — |

Les classements changent entre H1 et H2 — un modèle unique les mélangerait.

---

## Stack technique

- **Frontend** : SvelteKit + Tailwind CSS + Leaflet.js
- **Déploiement** : GitHub Pages (adapter-static)
- **Analyse** : Python (pandas, scikit-learn, statsmodels, matplotlib)
- **Modèle** : Double Hurdle (GLM logistique H1 + GLM logistique H2)

## Structure du projet

```
Etude gravité des accidents 974/
├── dashboard/                        ← Application SvelteKit
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/           ← Composants Svelte
│   │   │   │   ├── AccidentMap.svelte
│   │   │   │   ├── BarChart.svelte
│   │   │   │   ├── ForestPlot.svelte
│   │   │   │   ├── GravityBreakdown.svelte
│   │   │   │   ├── Hero.svelte
│   │   │   │   ├── HourlyChart.svelte
│   │   │   │   ├── HurdleExplainer.svelte
│   │   │   │   ├── ProfileCards.svelte
│   │   │   │   ├── RiskCalculator.svelte
│   │   │   │   ├── RiskFactors.svelte
│   │   │   │   └── StatGrid.svelte
│   │   │   ├── data/
│   │   │   │   ├── accidents.json      ← 934 accidents (extrait du BAAC)
│   │   │   │   ├── model-results.json  ← Résultats du modèle Double Hurdle
│   │   │   │   └── summaries.json      ← Statistiques agrégées
│   │   │   ├── stores/
│   │   │   │   └── filters.js          ← Store réactif des filtres
│   │   │   └── utils/
│   │   │       └── format.js           ← Fonctions de formatage
│   │   ├── routes/
│   │   │   ├── +layout.js
│   │   │   ├── +layout.svelte
│   │   │   └── +page.svelte            ← Page principale
│   │   ├── app.css
│   │   └── app.html
│   ├── scripts/
│   │   └── prepare_data.py             ← Prépare les JSON pour le dashboard
│   ├── svelte.config.js
│   ├── vite.config.js
│   └── package.json
├── data/
│   ├── data_raw/                       ← Fichiers BAAC bruts
│   │   ├── caract-2024.csv
│   │   ├── lieux-2024.csv
│   │   ├── usagers-2024.csv
│   │   ├── vehicules-2024.csv
│   │   ├── meteo_2024.csv
│   │   ├── H_974_previous-2020-2024.csv
│   │   └── 2024.csv
│   ├── data_processed/                 ← Données nettoyées et enrichies
│   │   ├── accidents_final.parquet
│   │   ├── accidents_meteo_974.parquet
│   │   ├── accidents_meteo_features.parquet
│   │   ├── baac_meteo_dataset.csv
│   │   ├── usagers_final.parquet
│   │   └── vehicules_final.parquet
│   └── data_geo/                       ← Données géographiques
│       ├── communes_974.geojson
│       └── routes_974_osm.json
├── scripts/                            ← Pipeline Python de préparation
│   ├── Step_1_filter.py                ← Filtrage et jointure BAAC 974
│   ├── step_2_meteo.py                 ← Enrichissement météo
│   ├── step_3_cumul-pluie.py           ← Calcul cumul de pluie
│   ├── step_4_usager-lieux-vehicules.py← Jointure usagers/lieux/véhicules
│   └── fix_geojson_974.py              ← Correction du GeoJSON communes
├── étude actuarielle.ipynb             ← Analyse statistique complète (Jupyter)
├── dashboard.html                      ← Export HTML standalone du dashboard
├── requirements.txt
└── README.md
```

## Installation

```bash
# Dépendances Python
pip install -r requirements.txt

# Lancer le pipeline de données (optionnel, données déjà générées)
python scripts/Step_1_filter.py
python scripts/step_2_meteo.py
python scripts/step_3_cumul-pluie.py
python scripts/step_4_usager-lieux-vehicules.py
python dashboard/scripts/prepare_data.py

# Dashboard SvelteKit
cd dashboard
npm install
npm run dev
```

## Déploiement GitHub Pages

1. Décommenter `base` dans `dashboard/svelte.config.js` et mettre le nom du repo
2. `cd dashboard && npm run build`
3. Pusher le dossier `build/` via GitHub Actions ou manuellement

Exemple de workflow `.github/workflows/deploy.yml` :

```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
        working-directory: dashboard
      - run: npm run build
        working-directory: dashboard
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dashboard/build
```

## Données

**Source** : [BAAC 2024 — ONISR / data.gouv.fr](https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere/)

Les données brutes sont dans `data/data_raw/`. Le pipeline `scripts/` les nettoie et les enrichit (météo, géolocalisation) vers `data/data_processed/`. Le script `dashboard/scripts/prepare_data.py` génère les JSON embarqués dans le dashboard.

## Limites

- Un seul millésime (2024) — pooler 2020–2024 pour stabiliser
- Petit effectif H2 (~43 tués) — intervalles de confiance larges
- Variables non observées (alcool, vitesse)
- Pas de données d'exposition (km parcourus)

---

*Projet réalisé dans le cadre d'une étude de sécurité routière — La Réunion 2024.*
