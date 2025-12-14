import pandas as pd
import numpy as np
from typing import List, Dict

df = pd.read_csv("../data/raw/eia_raw_data.csv")

print("Sample of the dataset\n", df.head())
print("\n")
print("Shape of the dataset: ", df.shape)
print("\n")

#information about the columns in the dataset and type of data in each column
df.info()

#checking for duplicates in the data
print("Duplicates before removal:", df.duplicated().sum())
df = df.drop_duplicates()
print("Duplicates after removal:", df.duplicated().sum())
print("\n")

#making the column nomenclatures a consistent pattern
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace("-", "_")
    .str.replace(" ", "_")
)

print("Columns after cleaning\n", df.columns)
print("\n")

#converting the time period column to datetime format
df['period'] = pd.to_datetime(df['period'])
print(df.head())
print("\n")

#checking for null values
print(df.isna().sum())

# using grouped data imputation technique for the cost and cost_per_btu columns as they have lot of null valyes
# but are extremely important for the project
# imputation is happening as:
# For a specific month -> for each specific fuel type -> the average of the cost for the specific fuel type for that 
# specific month to be imputed in the null fields of that specific fuel type for that specific month

def drop_unit_columns(df: pd.DataFrame) -> pd.DataFrame:
    unit_cols = [col for col in df.columns if col.endswith("_units")]
    return df.drop(columns=unit_cols)

df = drop_unit_columns(df)

df = df.drop(columns=["location", "statedescription"])

print(df.head())
print(df.shape)

numeric_cols = [col for col in df.columns if col not in ["period", "fueltypeid", "fueltypedescription", "sectordescription"]]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")


def impute_costs(df: pd.DataFrame, columns_to_impute: List[str] = None) -> pd.DataFrame:
    """
    Imputes missing fuel cost values using a hierarchical strategy:
    
    1. Monthly fuel-type mean       → (period, fueltypeid)
    2. Yearly fuel-type mean        → (year, fueltypeid)
    3. Global fuel-type mean        → (fueltypeid)

    Missing values fall back to the next layer ONLY if still NaN.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe containing cost fields.
    columns_to_impute : List[str], optional
        Target columns to impute. Defaults to ['cost', 'cost_per_btu'].

    Returns
    -------
    pd.DataFrame
        DataFrame with missing cost values imputed.
    """

    df = df.copy()

    if columns_to_impute is None:
        columns_to_impute = ["cost", "cost_per_btu"]

    df["year"] = df["period"].dt.year

    for col in columns_to_impute:

        df[col] = df.groupby(["period", "fueltypeid"])[col]\
                    .transform(lambda x: x.fillna(x.mean()))

        if df[col].isna().sum() > 0:
            df[col] = df.groupby(["year", "fueltypeid"])[col]\
                        .transform(lambda x: x.fillna(x.mean()))

        if df[col].isna().sum() > 0:
            df[col] = df.groupby("fueltypeid")[col]\
                        .transform(lambda x: x.fillna(x.mean()))

    return df

df_imputed = impute_costs(df, ["cost", "cost_per_btu"])

df_imputed = df_imputed.drop(columns=["stocks", "receipts", "receipts_btu"])
df_imputed = df_imputed.dropna(subset=['consumption_for_eg'])

print(df_imputed.head())
print("\n")
print(df_imputed.isna().sum())
print("\n")

numeric_cols = df_imputed.select_dtypes(include=np.number).columns
print((df_imputed[numeric_cols] < 0).sum())

output_path = "../data/processed/cleaned_data.csv"
df_imputed.to_csv(output_path, index=False)
print(f" Cleaned data saved to: {output_path}")