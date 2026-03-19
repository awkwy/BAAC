# 🏝️ Sécurité routière — La Réunion 2024

Dashboard interactif présentant les résultats d'une étude actuarielle sur les accidents corporels à La Réunion. Modèle **Double Hurdle** appliqué aux données **BAAC 2024** (ONISR) enrichies par **Météo France**.

## Aperçu

Ce projet transforme un notebook d'analyse actuarielle en une application web interactive destinée à un **public non technique**. L'approche éditoriale (scrollytelling) guide le lecteur à travers l'analyse :

1. **Cartographie** — Carte Leaflet des 934 accidents géolocalisés, colorés par gravité
2. **Profils** — Distribution des usagers, waffle chart, répartition horaire
3. **Facteurs de risque** — Comparaisons nuit/jour, urbain/rural, météo, collision
4. **Modèle Double Hurdle** — Explication visuelle du modèle en 2 étapes + forest plot des odds ratios
5. **Score de risque** — Calculateur interactif + profils-types
6. **Conclusions** — Synthèse et limites

## Stack technique

- **Framework** : SvelteKit 2 (Svelte 5 avec runes)
- **Carte** : Leaflet 1.9
- **Style** : CSS custom avec design tokens (thème éditorial clair)
- **Données** : JSON statique pré-calculé au build time
- **Déploiement** : adapter-static → Vercel / Netlify / GitHub Pages

## Installation

### Prérequis
- [Node.js](https://nodejs.org/) 18+ (LTS recommandé)
- [Python](https://www.python.org/) 3.8+ (pour le script de données)
- pandas (`pip install pandas`)

### Setup

```bash
# 1. Cloner le projet
git clone <repo-url>
cd reunion-dashboard

# 2. Installer les dépendances Node
npm install

# 3. Préparer les données (si pas déjà fait)
#    Place ton fichier baac_meteo_dataset.csv à la racine, puis :
python scripts/prepare_data.py baac_meteo_dataset.csv src/lib/data/

# 4. Lancer le serveur de développement
npm run dev

# Le site est accessible sur http://localhost:5173
```

### Build pour production

```bash
npm run build
# → Génère un site statique dans le dossier `build/`
# Ce dossier peut être déployé sur n'importe quel hébergeur statique
```

### Déploiement rapide sur Vercel

```bash
npx vercel
```

Ou connecte le repo GitHub à Vercel — il détectera automatiquement SvelteKit.

## Structure du projet

```
reunion-dashboard/
├── scripts/
│   └── prepare_data.py          # CSV → JSON (pipeline de données)
├── src/
│   ├── app.css                  # Design tokens, reset, typographie
│   ├── app.html                 # Shell HTML
│   ├── lib/
│   │   ├── components/
│   │   │   ├── AccidentMap.svelte      # Carte Leaflet interactive
│   │   │   ├── BarChart.svelte         # Bar chart horizontal réutilisable
│   │   │   ├── ForestPlot.svelte       # Forest plot (odds ratios)
│   │   │   ├── GravityBreakdown.svelte # Waffle chart des gravités
│   │   │   ├── Hero.svelte             # Section héro d'introduction
│   │   │   ├── HourlyChart.svelte      # Distribution horaire
│   │   │   ├── HurdleExplainer.svelte  # Diagramme explicatif du modèle
│   │   │   ├── ProfileCards.svelte     # Cartes profils-types
│   │   │   ├── RiskCalculator.svelte   # Calculateur de risque interactif
│   │   │   ├── RiskFactors.svelte      # Comparaisons de taux de gravité
│   │   │   └── StatGrid.svelte         # Grille de stats clés
│   │   ├── data/
│   │   │   ├── accidents.json          # 934 accidents géolocalisés
│   │   │   ├── model-results.json      # Résultats du Double Hurdle
│   │   │   └── summaries.json          # Agrégations pré-calculées
│   │   ├── stores/
│   │   │   └── filters.js              # État global des filtres (writable store)
│   │   └── utils/
│   │       └── format.js               # Formatage FR, labels BAAC, couleurs
│   └── routes/
│       ├── +layout.js                  # Config prerender
│       ├── +layout.svelte              # Layout racine
│       └── +page.svelte                # Page principale (scrollytelling)
├── package.json
├── svelte.config.js                    # Config SvelteKit + adapter-static
└── vite.config.js
```

## Données

Le fichier `baac_meteo_dataset.csv` (fourni séparément) contient 2 565 lignes (niveau usager) et 73 colonnes. Le script `prepare_data.py` produit 3 fichiers JSON optimisés :

| Fichier | Contenu | Taille |
|---------|---------|--------|
| `accidents.json` | 934 accidents avec lat/lon, gravité, conditions | ~174 KB |
| `summaries.json` | 16 tables d'agrégation pré-calculées | ~7 KB |
| `model-results.json` | Odds ratios, AUC, coefficients du modèle | ~5 KB |

## Résultats clés du modèle

**Hurdle 1 — P(grave | accident)** : AUC-ROC = 0,825 (43 variables)

**Hurdle 2 — P(tué | grave)** : AUC-ROC = 0,809 (4 variables sélectionnées par BIC)

| Variable | OR | IC 95% | Effet |
|----------|---:|--------|-------|
| Nuit | 3,75 | [1,69 – 8,29] | ×4 risque de décès |
| Équipement protecteur | 0,26 | [0,12 – 0,54] | ÷4 risque de décès |
| En agglomération | 0,25 | [0,12 – 0,53] | ÷4 risque de décès |
| Âge (+1 an) | 1,05 | [1,03 – 1,07] | +5% par année |

## Concepts Svelte utilisés

Ce projet utilise **Svelte 5** avec les nouvelles « runes » :

- `$state()` — état réactif local (ex : curseur d'âge, élément survolé)
- `$derived` — valeurs calculées automatiquement (ex : données filtrées)
- `$effect()` — effets de bord réactifs (ex : mise à jour des marqueurs Leaflet)
- `$props()` — déclaration des props d'un composant
- `$:` store subscriptions via `$filters` (auto-subscribe aux writable stores)

## Sources

- **BAAC 2024** — ONISR / data.gouv.fr — Département 974
- **Météo France** — Données horaires, stations de La Réunion
- **Contours communaux** — IGN / AdminExpress

## Licence

Données publiques (licence ouverte). Code du dashboard : usage libre.
