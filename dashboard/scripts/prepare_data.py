# Prépare les JSON consommés par le dashboard Svelte à partir du CSV BAAC+météo.
# Usage : python scripts/prepare_data.py <input.csv> <output_dir>

import pandas as pd
import numpy as np
import json
import sys
import os

def load_data(path):
    df = pd.read_csv(path)
    for col in ['lat', 'long']:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')
    return df

def build_accidents_json(df):
    grav_priority = {2: 4, 3: 3, 4: 2, 1: 1}  # 2=tué, 3=hosp, 4=blessé léger, 1=indemne
    df['_grav_priority'] = df['grav'].map(grav_priority)

    accidents = df.groupby('Num_Acc').agg(
        lat=('lat', 'first'),
        lon=('long', 'first'),
        grav_max=('grav', lambda x: x.iloc[x.map(grav_priority).values.argmax()]),
        n_usagers=('id_usager', 'count'),
        heure=('hrmn', 'first'),
        lum=('lum', 'first'),
        atm=('atm', 'first'),
        col=('col', 'first'),
        agg=('agg', 'first'),
        catv_main=('type_vehicule', 'first'),
        com=('com', 'first'),
        mois=('mois', 'first'),
        jour=('jour', 'first'),
        surf=('surf', 'first'),
        pluie_mm=('pluie_mm', 'first'),
        temperature=('temperature', 'first'),
        nuit=('nuit', 'max'),
        weekend=('weekend', 'max'),
    ).reset_index()

    accidents = accidents.dropna(subset=['lat', 'lon'])

    records = []
    for _, r in accidents.iterrows():
        records.append({
            'id': str(r['Num_Acc']),
            'lat': round(float(r['lat']), 5) if pd.notna(r['lat']) else None,
            'lon': round(float(r['lon']), 5) if pd.notna(r['lon']) else None,
            'g': int(r['grav_max']),
            'n': int(r['n_usagers']),
            'h': str(r['heure']) if pd.notna(r['heure']) else None,
            'lum': int(r['lum']) if pd.notna(r['lum']) else None,
            'atm': int(r['atm']) if pd.notna(r['atm']) else None,
            'col': int(r['col']) if pd.notna(r['col']) else None,
            'agg': int(r['agg']) if pd.notna(r['agg']) else None,
            'veh': str(r['catv_main']) if pd.notna(r['catv_main']) else 'autre',
            'com': int(r['com']) if pd.notna(r['com']) else None,
            'mois': int(r['mois']) if pd.notna(r['mois']) else None,
            'nuit': int(r['nuit']) if pd.notna(r['nuit']) else 0,
            'wkd': int(r['weekend']) if pd.notna(r['weekend']) else 0,
            'pluie': round(float(r['pluie_mm']), 1) if pd.notna(r['pluie_mm']) else None,
            'temp': round(float(r['temperature']), 1) if pd.notna(r['temperature']) else None,
        })

    return records

def build_summaries(df):
    summaries = {}

    summaries['total_usagers'] = len(df)
    summaries['total_accidents'] = df['Num_Acc'].nunique()
    n_graves = int(df['grave'].sum())
    n_tues = int((df['grav'] == 2).sum())
    n_hosp = int((df['grav'] == 3).sum())
    n_bl = int((df['grav'] == 4).sum())
    n_ind = int((df['grav'] == 1).sum())
    summaries['gravity_distribution'] = {
        'indemne': n_ind,
        'blesse_leger': n_bl,
        'hospitalise': n_hosp,
        'tue': n_tues,
        'grave_total': n_graves,
        'pct_grave': round(n_graves / len(df) * 100, 1)
    }

    age_grav = df.groupby('age_groupe').agg(
        total=('grave', 'count'),
        graves=('grave', 'sum'),
        tues=('grav', lambda x: (x == 2).sum())
    ).reset_index()
    age_grav['taux_grav'] = (age_grav['graves'] / age_grav['total'] * 100).round(1)
    summaries['by_age'] = age_grav.to_dict('records')

    veh_grav = df.groupby('type_vehicule').agg(
        total=('grave', 'count'),
        graves=('grave', 'sum'),
        tues=('grav', lambda x: (x == 2).sum())
    ).reset_index().sort_values('total', ascending=False)
    veh_grav['taux_grav'] = (veh_grav['graves'] / veh_grav['total'] * 100).round(1)
    summaries['by_vehicle'] = veh_grav.to_dict('records')

    sex_grav = df.groupby('sexe_label').agg(
        total=('grave', 'count'),
        graves=('grave', 'sum')
    ).reset_index()
    sex_grav['taux_grav'] = (sex_grav['graves'] / sex_grav['total'] * 100).round(1)
    summaries['by_sex'] = sex_grav.to_dict('records')

    hourly = df.groupby('heure').agg(
        total=('grave', 'count'),
        graves=('grave', 'sum'),
        tues=('grav', lambda x: (x == 2).sum())
    ).reset_index()
    hourly['taux_grav'] = (hourly['graves'] / hourly['total'] * 100).round(1)
    hourly['heure'] = hourly['heure'].astype(int)
    summaries['hourly'] = hourly.sort_values('heure').to_dict('records')

    lum_grav = df.groupby('eclairage').agg(
        total=('grave', 'count'),
        graves=('grave', 'sum')
    ).reset_index()
    lum_grav['taux_grav'] = (lum_grav['graves'] / lum_grav['total'] * 100).round(1)
    summaries['by_lighting'] = lum_grav.sort_values('total', ascending=False).to_dict('records')

    atm_grav = df.groupby('atm_groupe').agg(
        total=('grave', 'count'),
        graves=('grave', 'sum')
    ).reset_index()
    atm_grav['taux_grav'] = (atm_grav['graves'] / atm_grav['total'] * 100).round(1)
    summaries['by_weather'] = atm_grav.sort_values('total', ascending=False).to_dict('records')

    col_grav = df.groupby('type_collision').agg(
        total=('grave', 'count'),
        graves=('grave', 'sum')
    ).reset_index()
    col_grav['taux_grav'] = (col_grav['graves'] / col_grav['total'] * 100).round(1)
    summaries['by_collision'] = col_grav.sort_values('total', ascending=False).to_dict('records')

    night_grav = df.groupby('nuit').agg(
        total=('grave', 'count'),
        graves=('grave', 'sum'),
        tues=('grav', lambda x: (x == 2).sum())
    ).reset_index()
    night_grav['taux_grav'] = (night_grav['graves'] / night_grav['total'] * 100).round(1)
    summaries['night_vs_day'] = night_grav.to_dict('records')

    agglo_grav = df.groupby('en_agglomeration').agg(
        total=('grave', 'count'),
        graves=('grave', 'sum'),
        tues=('grav', lambda x: (x == 2).sum())
    ).reset_index()
    agglo_grav['taux_grav'] = (agglo_grav['graves'] / agglo_grav['total'] * 100).round(1)
    summaries['agglo_vs_rural'] = agglo_grav.to_dict('records')

    route_grav = df.groupby('type_route').agg(
        total=('grave', 'count'),
        graves=('grave', 'sum')
    ).reset_index()
    route_grav['taux_grav'] = (route_grav['graves'] / route_grav['total'] * 100).round(1)
    summaries['by_route'] = route_grav.sort_values('total', ascending=False).to_dict('records')

    role_grav = df.groupby('role').agg(
        total=('grave', 'count'),
        graves=('grave', 'sum'),
        tues=('grav', lambda x: (x == 2).sum())
    ).reset_index()
    role_grav['taux_grav'] = (role_grav['graves'] / role_grav['total'] * 100).round(1)
    summaries['by_role'] = role_grav.to_dict('records')

    monthly = df.groupby('mois').agg(
        total=('Num_Acc', lambda x: x.nunique()),
        usagers=('grave', 'count'),
        graves=('grave', 'sum')
    ).reset_index()
    monthly['taux_grav'] = (monthly['graves'] / monthly['usagers'] * 100).round(1)
    summaries['monthly'] = monthly.sort_values('mois').to_dict('records')

    com_stats = df.groupby('com').agg(
        total=('grave', 'count'),
        graves=('grave', 'sum'),
        tues=('grav', lambda x: (x == 2).sum())
    ).reset_index()
    com_stats['taux_grav'] = (com_stats['graves'] / com_stats['total'] * 100).round(1)
    com_stats['com'] = com_stats['com'].astype(int)
    summaries['by_commune'] = com_stats.sort_values('total', ascending=False).to_dict('records')

    return summaries

def build_model_results():
    return {
        "description": "Double Hurdle model — La Réunion 2024",
        "population": {
            "total_usagers": 2493,
            "graves_h1": 425,
            "pct_graves": 17.0,
            "tues_h2": 43,
            "pct_tues_parmi_graves": 10.1
        },
        "hurdle1": {
            "name": "P(grave | accident)",
            "method": "GLM Logistique Ridge (L2), balanced class weights",
            "n_features": 43,
            "auc_roc_cv": {"mean": 0.8250, "std": 0.0219},
            "auc_roc_test": 0.7984,
            "gini": 0.5968,
            "brier": 0.1831,
            "top_aggravating": [
                {"feature": "2RM >125cm³", "OR": 3.12, "label": "Moto > 125cm³"},
                {"feature": "piéton", "OR": 2.85, "label": "Piéton"},
                {"feature": "vélo/VAE", "OR": 2.64, "label": "Vélo / VAE"},
                {"feature": "nuit sans éclairage", "OR": 2.31, "label": "Nuit sans éclairage"},
                {"feature": "sans collision", "OR": 2.18, "label": "Sans collision (seul)"},
                {"feature": "2RM 50-125cm³", "OR": 1.95, "label": "Moto 50-125cm³"},
                {"feature": "frontale", "OR": 1.82, "label": "Collision frontale"},
                {"feature": "nuit éclairage allumé", "OR": 1.74, "label": "Nuit éclairée"},
                {"feature": "hors agglomération", "OR": 1.55, "label": "Hors agglomération"},
                {"feature": "pluie", "OR": 1.38, "label": "Temps pluvieux"}
            ],
            "top_protective": [
                {"feature": "voiture", "OR": 0.42, "label": "Voiture"},
                {"feature": "passager", "OR": 0.58, "label": "Passager"},
                {"feature": "ceinture", "OR": 0.62, "label": "Ceinture attachée"},
                {"feature": "en agglomération", "OR": 0.65, "label": "En agglomération"},
                {"feature": "collision arrière", "OR": 0.71, "label": "Collision arrière"}
            ]
        },
        "hurdle2": {
            "name": "P(tué | grave)",
            "method": "GLM Logistique Ridge, stepwise BIC selection",
            "n_features": 4,
            "variables": ["equip_bin_protégé", "age", "nuit", "en_agglomeration"],
            "epv": 10.8,
            "auc_roc_cv": {"mean": 0.8087, "std": 0.1248},
            "aic": 233.8,
            "bic": 254.0,
            "odds_ratios": [
                {
                    "variable": "equip_bin_protégé",
                    "label": "Équipement de protection",
                    "beta": -1.355,
                    "OR": 0.26,
                    "CI_lo": 0.12,
                    "CI_hi": 0.54,
                    "p": 0.0003,
                    "interpretation": "Porter un casque ou une ceinture divise le risque de décès par 4"
                },
                {
                    "variable": "age",
                    "label": "Âge (+1 an)",
                    "beta": 0.048,
                    "OR": 1.05,
                    "CI_lo": 1.03,
                    "CI_hi": 1.07,
                    "p": 0.0000,
                    "interpretation": "Chaque année supplémentaire augmente le risque de décès de 5%"
                },
                {
                    "variable": "nuit",
                    "label": "Accident de nuit",
                    "beta": 1.321,
                    "OR": 3.75,
                    "CI_lo": 1.69,
                    "CI_hi": 8.29,
                    "p": 0.0011,
                    "interpretation": "La nuit quadruple le risque de décès"
                },
                {
                    "variable": "en_agglomeration",
                    "label": "En agglomération",
                    "beta": -1.394,
                    "OR": 0.25,
                    "CI_lo": 0.12,
                    "CI_hi": 0.53,
                    "p": 0.0003,
                    "interpretation": "Être en ville divise le risque de décès par 4"
                }
            ],
            "expert_model": {
                "variables": ["role", "age", "nuit", "en_agglomeration"],
                "odds_ratios": [
                    {"variable": "role_piéton", "label": "Piéton", "OR": 3.41, "CI_lo": 1.35, "CI_hi": 8.60, "p": 0.0093},
                    {"variable": "role_passager", "label": "Passager", "OR": 1.07, "CI_lo": 0.37, "CI_hi": 3.11, "p": 0.9058},
                    {"variable": "age", "label": "Âge (+1 an)", "OR": 1.04, "CI_lo": 1.02, "CI_hi": 1.06, "p": 0.0002},
                    {"variable": "nuit", "label": "Nuit", "OR": 4.51, "CI_lo": 2.07, "CI_hi": 9.85, "p": 0.0002},
                    {"variable": "en_agglomeration", "label": "En agglo.", "OR": 0.27, "CI_lo": 0.13, "CI_hi": 0.58, "p": 0.0007}
                ]
            }
        },
        "composite_score": {
            "alpha": 4.0,
            "ratio_max_min": 16.0,
            "description": "Score = P(grave) × [α × P(tué|grave) + (1-α)×P(hosp|grave)]"
        },
        "validation": {
            "brant_test": "49% des variables violent l'hypothèse PO → modèle ordinal unique rejeté",
            "spearman": "Rankings H1 vs H2 divergents (p > 0.05) → les deux hurdles captent des mécanismes différents",
            "gam_check": "EDF ≈ 0.6 → relation quasi-linéaire, GLM suffisant"
        }
    }


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else 'baac_meteo_dataset.csv'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'src/lib/data'

    os.makedirs(output_dir, exist_ok=True)

    print(f"Loading data from {input_path}...")
    df = load_data(input_path)
    print(f"  → {len(df)} rows, {len(df.columns)} columns")

    print("Building accidents.json (accident-level)...")
    accidents = build_accidents_json(df)
    with open(os.path.join(output_dir, 'accidents.json'), 'w') as f:
        json.dump(accidents, f, separators=(',', ':'))
    print(f"  → {len(accidents)} accidents")

    print("Building summaries.json (pre-aggregated stats)...")
    summaries = build_summaries(df)
    with open(os.path.join(output_dir, 'summaries.json'), 'w') as f:
        json.dump(summaries, f, separators=(',', ':'), ensure_ascii=False)
    print(f"  → {len(summaries)} summary tables")

    print("Building model-results.json (Double Hurdle outputs)...")
    model = build_model_results()
    with open(os.path.join(output_dir, 'model-results.json'), 'w') as f:
        json.dump(model, f, separators=(',', ':'), ensure_ascii=False, indent=2)
    print("  → done")

    print("\n✓ All JSON files written to", output_dir)


if __name__ == '__main__':
    main()
