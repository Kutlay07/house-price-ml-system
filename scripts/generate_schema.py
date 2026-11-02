import pandas as pd


df = pd.read_csv("test.csv")

aliases = {
    "1stFlrSF": "first_flr_sf",
    "2ndFlrSF": "second_flr_sf",
    "3SsnPorch": "three_ssn_porch",
}

print("from pydantic import BaseModel, Field")
print()
print()
print("class HouseFeatures(BaseModel):")
for col, dtype in df.dtypes.items():
    if col == "Id":
        continue

    has_missing = df[col].isna().any()

    if pd.api.types.is_integer_dtype(dtype):
        py_type = "int"

    elif pd.api.types.is_float_dtype(dtype):
        py_type = "float"

    else:
        py_type = "str"

    if has_missing:
        py_type += " | None"

    if col in aliases:
        field_name = aliases[col]

        if has_missing:
            print(
                f'    {field_name}: {py_type} = '
                f'Field(default=None, alias="{col}")'
            )
        else:
            print(
                f'    {field_name}: {py_type} = '
                f'Field(alias="{col}")'
            )

    else:
        if has_missing:
            print(f"    {col}: {py_type} = None")
        else:
            print(f"    {col}: {py_type}")
