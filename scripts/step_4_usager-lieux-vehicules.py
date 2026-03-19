import pandas as pd

df_floor = pd.read_parquet(
    "../data/data_processed/accidents_meteo_features.parquet"
)

lieux = pd.read_csv(
    "../data/data_raw/lieux-2024.csv",
    sep=";",
    dtype=str
)

vehicules = pd.read_csv(
    "../data/data_raw/vehicules-2024.csv",
    sep=";",
    dtype=str
)

usagers = pd.read_csv(
    "../data/data_raw/usagers-2024.csv",
    sep=";",
    dtype=str
)

lieux_974 = lieux[
    lieux["Num_Acc"].isin(df_floor["Num_Acc"])
]

vehicules_974 = vehicules[
    vehicules["Num_Acc"].isin(df_floor["Num_Acc"])
]

usagers_974 = usagers[
    usagers["Num_Acc"].isin(df_floor["Num_Acc"])
]

df_accidents = df_floor.merge(
    lieux_974,
    on="Num_Acc",
    how="left"
)

df_veh = vehicules_974.merge(
    df_accidents,
    on="Num_Acc",
    how="left"
)

df_usagers = usagers_974.merge(
    df_veh,
    on=["Num_Acc","id_vehicule"],
    how="left"
)

df_usagers["grave"] = df_usagers["grav"].isin(["2","3"]).astype(int)

df_usagers["age"] = 2024 - pd.to_numeric(
    df_usagers["an_nais"],
    errors="coerce"
)

df_usagers["rain"] = (
    pd.to_numeric(df_usagers["RR1"], errors="coerce") > 0
).astype(int)

df_usagers["wind_gust"] = df_usagers[
    ["FXY","FXI"]
].apply(pd.to_numeric, errors="coerce").max(axis=1)

df_usagers["visibility_low"] = (
    pd.to_numeric(df_usagers["VV"], errors="coerce") < 2000
).astype(int)

print("Accidents :", df_accidents.shape)
print("Vehicules :", df_veh.shape)
print("Usagers :", df_usagers.shape)

df_accidents.to_parquet(
    "../data/data_processed/accidents_final.parquet",
    index=False
)

df_veh.to_parquet(
    "../data/data_processed/vehicules_final.parquet",
    index=False
)

df_usagers.to_parquet(
    "../data/data_processed/usagers_final.parquet",
    index=False
)

print("Datasets exportés")