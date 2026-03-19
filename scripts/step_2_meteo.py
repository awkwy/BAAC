import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):

    R = 6371  # rayon terre km

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c


print("Chargement BAAC")

caract = pd.read_csv(
    r"..\data\data_raw\caract-2024.csv",
    sep=";",
    dtype=str
)

# accidents Réunion
caract_974 = caract[caract["dep"] == "974"].copy()


print("Construction datetime accident")

hrmn = caract_974["hrmn"].astype(str).str.strip()

caract_974["acc_datetime"] = pd.to_datetime(
    caract_974["an"] + "-" +
    caract_974["mois"].str.zfill(2) + "-" +
    caract_974["jour"].str.zfill(2) + " " +
    hrmn,
    errors="coerce"
)

caract_974["hour_floor"] = caract_974["acc_datetime"].dt.floor("h")
caract_974["hour_ceil"] = caract_974["acc_datetime"].dt.ceil("h")


print("Nettoyage coordonnées")

caract_974["lat"] = (
    caract_974["lat"]
    .str.replace(",", ".")
    .astype(float)
)

caract_974["long"] = (
    caract_974["long"]
    .str.replace(",", ".")
    .astype(float)
)


print("Chargement météo")

meteo = pd.read_csv(
    r"..\data\data_raw\meteo_2024.csv",
    sep=";",
    low_memory=False
)

meteo["meteo_datetime_hour"] = pd.to_datetime(
    meteo["AAAAMMJJHH"].astype(str),
    format="%Y%m%d%H",
    errors="coerce"
)

# colonnes utiles
meteo_key = meteo[[
    "NUM_POSTE",
    "LAT",
    "LON",
    "meteo_datetime_hour",
    "RR1",
    "FF",
    "FXY",
    "FXI",
    "T",
    "U",
    "VV"
]].copy()

meteo_key["NUM_POSTE"] = meteo_key["NUM_POSTE"].astype(str)


stations = meteo_key[["NUM_POSTE", "LAT", "LON"]].drop_duplicates()


print("Recherche station la plus proche")

nearest_station = []
nearest_distance = []

for idx, row in caract_974.iterrows():

    lat = row["lat"]
    lon = row["long"]

    if pd.isna(lat) or pd.isna(lon):

        nearest_station.append(np.nan)
        nearest_distance.append(np.nan)
        continue

    distances = stations.apply(
        lambda x: haversine(lat, lon, x["LAT"], x["LON"]),
        axis=1
    )

    min_idx = distances.idxmin()

    nearest_station.append(stations.loc[min_idx, "NUM_POSTE"])
    nearest_distance.append(distances[min_idx])

caract_974["NUM_POSTE"] = nearest_station
caract_974["dist_station_km"] = nearest_distance


print("Merge météo")

meteo_merge = meteo_key.drop(columns=["LAT", "LON"])

df_floor = caract_974.merge(
    meteo_merge,
    left_on=["NUM_POSTE", "hour_floor"],
    right_on=["NUM_POSTE", "meteo_datetime_hour"],
    how="left"
)

df_ceil = caract_974.merge(
    meteo_merge,
    left_on=["NUM_POSTE", "hour_ceil"],
    right_on=["NUM_POSTE", "meteo_datetime_hour"],
    how="left"
)


df_floor["rain_meteo"] = (
    pd.to_numeric(df_floor["RR1"], errors="coerce") > 0
).astype(int)

df_ceil["rain_meteo"] = (
    pd.to_numeric(df_ceil["RR1"], errors="coerce") > 0
).astype(int)


rain_codes = ["2", "3"]

df_floor["rain_baac"] = df_floor["atm"].isin(rain_codes).astype(int)
df_ceil["rain_baac"] = df_ceil["atm"].isin(rain_codes).astype(int)


print("Comparaison pluie")

tab_floor = pd.crosstab(
    df_floor["rain_baac"],
    df_floor["rain_meteo"]
)

tab_ceil = pd.crosstab(
    df_ceil["rain_baac"],
    df_ceil["rain_meteo"]
)

print("------ FLOOR ------")
print(tab_floor)

print("------ CEIL ------")
print(tab_ceil)


def score_alignment(df):

    tp = ((df["rain_baac"] == 1) & (df["rain_meteo"] == 1)).sum()
    tn = ((df["rain_baac"] == 0) & (df["rain_meteo"] == 0)).sum()

    total = len(df)

    return (tp + tn) / total


score_floor = score_alignment(df_floor)
score_ceil = score_alignment(df_ceil)

print("Score FLOOR :", score_floor)
print("Score CEIL :", score_ceil)


print("Distance moyenne station :", caract_974["dist_station_km"].mean())

df_floor.to_parquet(
    r"..\data\data_processed\accidents_meteo_974.parquet",
    index=False
)