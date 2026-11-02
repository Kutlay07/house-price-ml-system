import numpy as np


def prepare_features(df):
    df = df.copy()

    structural_fill = {
        "PoolQC": "No Pool",
        "MiscFeature": "None",
        "Alley": "No Alley",
        "Fence": "No Fence",
        "FireplaceQu": "No Fireplace",
        "GarageType": "No Garage",
        "GarageFinish": "No Garage",
        "GarageQual": "No Garage",
        "GarageCond": "No Garage",
        "BsmtQual": "No Basement",
        "BsmtCond": "No Basement",
        "BsmtFinType1": "No Basement",
    }

    for col in structural_fill:
        if col in df.columns:
            df[col] = df[col].astype("object")

    df = df.fillna(value=structural_fill)

    no_basement = df["TotalBsmtSF"] == 0

    df.loc[no_basement, ["BsmtExposure", "BsmtFinType2"]] = (
        df.loc[no_basement, ["BsmtExposure", "BsmtFinType2"]]
        .fillna("No Basement")
    )

    df["HasGarage"] = (df["GarageArea"] > 0).astype(int)
    df["GarageYrBlt"] = df["GarageYrBlt"].fillna(0)

    df["TotalSF"] = (
        df["TotalBsmtSF"]
        + df["1stFlrSF"]
        + df["2ndFlrSF"]
    )

    df["HouseAge"] = df["YrSold"] - df["YearBuilt"]

    df["RemodAge"] = (
        df["YrSold"] - df["YearRemodAdd"]
    ).clip(lower=0)

    df["GarageAge"] = np.where(
        df["HasGarage"] == 1,
        df["YrSold"] - df["GarageYrBlt"],
        0,
    )

    df["TotalBathrooms"] = (
        df["FullBath"]
        + df["BsmtFullBath"]
        + 0.5 * df["HalfBath"]
        + 0.5 * df["BsmtHalfBath"]
    )

    return df
