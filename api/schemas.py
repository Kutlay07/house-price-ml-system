from pydantic import BaseModel, Field


class HouseFeatures(BaseModel):
    MSSubClass: int
    MSZoning: str | None = None
    LotFrontage: float | None = None
    LotArea: int
    Street: str
    Alley: str | None = None
    LotShape: str
    LandContour: str
    Utilities: str | None = None
    LotConfig: str
    LandSlope: str
    Neighborhood: str
    Condition1: str
    Condition2: str
    BldgType: str
    HouseStyle: str
    OverallQual: int
    OverallCond: int
    YearBuilt: int
    YearRemodAdd: int
    RoofStyle: str
    RoofMatl: str
    Exterior1st: str | None = None
    Exterior2nd: str | None = None
    MasVnrType: str | None = None
    MasVnrArea: float | None = None
    ExterQual: str
    ExterCond: str
    Foundation: str
    BsmtQual: str | None = None
    BsmtCond: str | None = None
    BsmtExposure: str | None = None
    BsmtFinType1: str | None = None
    BsmtFinSF1: float | None = None
    BsmtFinType2: str | None = None
    BsmtFinSF2: float | None = None
    BsmtUnfSF: float | None = None
    TotalBsmtSF: float | None = None
    Heating: str
    HeatingQC: str
    CentralAir: str
    Electrical: str
    first_flr_sf: int = Field(alias="1stFlrSF")
    second_flr_sf: int = Field(alias="2ndFlrSF")
    LowQualFinSF: int
    GrLivArea: int
    BsmtFullBath: float | None = None
    BsmtHalfBath: float | None = None
    FullBath: int
    HalfBath: int
    BedroomAbvGr: int
    KitchenAbvGr: int
    KitchenQual: str | None = None
    TotRmsAbvGrd: int
    Functional: str | None = None
    Fireplaces: int
    FireplaceQu: str | None = None
    GarageType: str | None = None
    GarageYrBlt: float | None = None
    GarageFinish: str | None = None
    GarageCars: float | None = None
    GarageArea: float | None = None
    GarageQual: str | None = None
    GarageCond: str | None = None
    PavedDrive: str
    WoodDeckSF: int
    OpenPorchSF: int
    EnclosedPorch: int
    three_ssn_porch: int = Field(alias="3SsnPorch")
    ScreenPorch: int
    PoolArea: int
    PoolQC: str | None = None
    Fence: str | None = None
    MiscFeature: str | None = None
    MiscVal: int
    MoSold: int
    YrSold: int
    SaleType: str | None = None
    SaleCondition: str
