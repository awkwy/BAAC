import pandas as pd


print("Chargement données")


# Charger météo brute (horaire)


meteo = pd.read_csv(
    "../data/data_raw/meteo_2024.csv",
    sep=";",
    low_memory=False
)

meteo["RR1"] = pd.to_numeric(meteo["RR1"], errors="coerce")

meteo["meteo_datetime_hour"] = pd.to_datetime(
    meteo["AAAAMMJJHH"].astype(str),
    format="%Y%m%d%H",
    errors="coerce"
)

# garder colonnes utiles
meteo = meteo[[
    "NUM_POSTE",
    "meteo_datetime_hour",
    "RR1"
]]

meteo["NUM_POSTE"] = meteo["NUM_POSTE"].astype(str)

# Trier série temporelle


meteo = meteo.sort_values(
    ["NUM_POSTE", "meteo_datetime_hour"]
)

# Cumuls pluie 


print("Calcul cumuls pluie")

meteo["rain_3h"] = (
    meteo
    .groupby("NUM_POSTE")["RR1"]
    .rolling(3, min_periods=1)
    .sum()
    .reset_index(level=0, drop=True)
)

meteo["rain_6h"] = (
    meteo
    .groupby("NUM_POSTE")["RR1"]
    .rolling(6, min_periods=1)
    .sum()
    .reset_index(level=0, drop=True)
)

meteo["rain_24h"] = (
    meteo
    .groupby("NUM_POSTE")["RR1"]
    .rolling(24, min_periods=1)
    .sum()
    .reset_index(level=0, drop=True)
)


# Charger accidents


print("Chargement accidents")

accidents = pd.read_parquet(
    "../data/data_processed/accidents_meteo_974.parquet"
)

accidents["NUM_POSTE"] = accidents["NUM_POSTE"].astype(str)


# Jointure météo cumulée

print("Jointure météo")

df = accidents.merge(
    meteo,
    on=["NUM_POSTE","meteo_datetime_hour"],
    how="left",
    suffixes=("", "_meteo")
)


# Variables utiles


df["rain"] = (df["RR1_meteo"] > 0).astype(int)
print(
    df[["RR1_meteo","rain_3h","rain_6h","rain_24h"]].head()
)
df["rain_3h_flag"] = (df["rain_3h"] > 0).astype(int)


# Export


df.to_parquet(
    "../data/data_processed/accidents_meteo_features.parquet",
    index=False
)

print("Dataset météo enrichi exporté")