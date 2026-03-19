"""
Corrige le GeoJSON France-GeoJSON de La Reunion (974).
Le fichier source a les polygones melanges : les codes INSEE ne correspondent
pas aux bons polygones geographiques (12 erreurs sur 24).

Ce script reassigne les codes et les noms aux bons polygones en utilisant
les centroides geographiques connus de chaque commune.

Usage :
    python fix_geojson_974.py
    python fix_geojson_974.py chemin/vers/communes_974.geojson
"""

import json
import sys
import os
import math

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PATH = os.path.join(PROJECT_ROOT, 'data', 'data_geo', 'communes_974.geojson')

# Positions geographiques connues des communes (centroides approximatifs)
# Source : carte administrative officielle + OpenStreetMap
COMMUNES_REF = {
    '97401': {'nom': 'Les Avirons',          'lon': 55.330, 'lat': -21.240},
    '97402': {'nom': 'Bras-Panon',           'lon': 55.650, 'lat': -21.020},
    '97403': {'nom': 'Cilaos',               'lon': 55.470, 'lat': -21.130},
    '97404': {'nom': 'Entre-Deux',           'lon': 55.470, 'lat': -21.230},
    '97405': {'nom': "L'Etang-Sale",         'lon': 55.350, 'lat': -21.270},
    '97406': {'nom': 'Petite-Ile',           'lon': 55.570, 'lat': -21.350},
    '97407': {'nom': 'Le Port',              'lon': 55.300, 'lat': -20.940},
    '97408': {'nom': 'La Possession',        'lon': 55.350, 'lat': -20.920},
    '97409': {'nom': 'Saint-Andre',          'lon': 55.660, 'lat': -20.960},
    '97410': {'nom': 'Saint-Benoit',         'lon': 55.700, 'lat': -21.080},
    '97411': {'nom': 'Saint-Denis',          'lon': 55.450, 'lat': -20.880},
    '97412': {'nom': 'Saint-Joseph',         'lon': 55.630, 'lat': -21.370},
    '97413': {'nom': 'Saint-Leu',            'lon': 55.290, 'lat': -21.170},
    '97414': {'nom': 'Saint-Louis',          'lon': 55.420, 'lat': -21.280},
    '97415': {'nom': 'Saint-Paul',           'lon': 55.280, 'lat': -21.020},
    '97416': {'nom': 'Saint-Pierre',         'lon': 55.480, 'lat': -21.330},
    '97417': {'nom': 'Sainte-Marie',         'lon': 55.540, 'lat': -20.900},
    '97418': {'nom': 'Sainte-Rose',          'lon': 55.780, 'lat': -21.150},
    '97419': {'nom': 'Sainte-Suzanne',       'lon': 55.600, 'lat': -20.920},
    '97420': {'nom': 'Le Tampon',            'lon': 55.520, 'lat': -21.250},
    '97421': {'nom': 'Salazie',              'lon': 55.520, 'lat': -21.040},
    '97422': {'nom': 'Trois-Bassins',        'lon': 55.300, 'lat': -21.100},
    '97423': {'nom': 'Plaine-des-Palmistes', 'lon': 55.630, 'lat': -21.150},
    '97424': {'nom': 'Saint-Philippe',       'lon': 55.730, 'lat': -21.360},
}


def _centroid(geometry):
    polys = []
    if geometry['type'] == 'Polygon':
        polys.append(geometry['coordinates'][0])
    elif geometry['type'] == 'MultiPolygon':
        for p in geometry['coordinates']:
            polys.append(p[0])
    if not polys:
        return None, None
    main = max(polys, key=len)
    lons = [pt[0] for pt in main]
    lats = [pt[1] for pt in main]
    return sum(lons)/len(lons), sum(lats)/len(lats)


def _distance(lon1, lat1, lon2, lat2):
    return math.sqrt((lon1 - lon2)**2 + (lat1 - lat2)**2)


def fix_geojson(path):
    with open(path, 'r', encoding='utf-8') as f:
        geo = json.load(f)

    features = geo['features']

    # Centroide de chaque polygone
    poly_centroids = []
    for i, feat in enumerate(features):
        cx, cy = _centroid(feat['geometry'])
        poly_centroids.append((i, cx, cy))

    # Matching glouton : assigner chaque commune au polygone le plus proche
    all_pairs = []
    for code, ref in COMMUNES_REF.items():
        for i, cx, cy in poly_centroids:
            if cx is None:
                continue
            d = _distance(cx, cy, ref['lon'], ref['lat'])
            all_pairs.append((d, code, i))
    all_pairs.sort()

    assignments = {}
    used_codes = set()
    used_polys = set()
    for d, code, poly_idx in all_pairs:
        if code in used_codes or poly_idx in used_polys:
            continue
        assignments[poly_idx] = code
        used_codes.add(code)
        used_polys.add(poly_idx)

    # Appliquer
    n_changed = 0
    for poly_idx, correct_code in assignments.items():
        feat = features[poly_idx]
        old_code = str(feat['properties'].get('code', '?'))
        correct_nom = COMMUNES_REF[correct_code]['nom']

        nom_key = 'nom'
        for k in ['nom', 'NOM', 'name']:
            if k in feat['properties']:
                nom_key = k
                break
        old_nom = feat['properties'].get(nom_key, '?')

        if old_code != correct_code or old_nom != correct_nom:
            print(f"  {old_code:5s} -> {correct_code}  |  {old_nom:25s} -> {correct_nom}")
            feat['properties']['code'] = correct_code
            feat['properties'][nom_key] = correct_nom
            n_changed += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(geo, f, ensure_ascii=False)

    print(f"\n{n_changed} polygones corriges - fichier ecrase : {path}")


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    if not os.path.exists(path):
        print(f"Fichier introuvable : {path}")
        sys.exit(1)
    fix_geojson(path)