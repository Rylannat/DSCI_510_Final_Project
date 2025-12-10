import pandas as pd

# Data Loading Function
def load_cleaned_data(path: str) -> pd.DataFrame:
    """
    Load the cleaned dataset and ensure proper types.
    
    Parameters
    ----------
    path : str
        Path to the cleaned CSV file.
        
    Returns
    -------
    pd.DataFrame
        Cleaned dataframe with datetime and year column.
    """
    df = pd.read_csv(path)
    return df

# 1. Time-Series Aggregation
def compute_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute monthly aggregated metrics.
    
    Returns sum for generation/consumption and mean for cost, heat_content, sulfur_content.
    """
    monthly = df.groupby('period').agg({
        'generation': 'sum',
        'total_consumption': 'sum',
        'consumption_for_eg': 'sum',
        'consumption_uto': 'sum',
        'cost': 'mean',
        'cost_per_btu': 'mean',
        'heat_content': 'mean',
        'sulfur_content': 'mean'
    }).reset_index()
    return monthly

def compute_yearly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute yearly aggregated metrics.
    """
    yearly = df.groupby('year').agg({
        'generation': 'sum',
        'total_consumption': 'sum',
        'consumption_for_eg': 'sum',
        'consumption_uto': 'sum',
        'cost': 'mean',
        'cost_per_btu': 'mean',
        'heat_content': 'mean',
        'sulfur_content': 'mean'
    }).reset_index()
    return yearly

# 2. Fuel-Type Analysis
def compute_fuel_type_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize metrics by fuel type and compute efficiency.
    
    Efficiency is calculated as generation / total_consumption.
    """
    fuel_type_summary = df.groupby('fueltypedescription').agg({
        'generation': 'sum',
        'total_consumption': 'sum',
        'consumption_for_eg': 'sum',
        'consumption_uto': 'sum',
        'cost': 'mean',
        'cost_per_btu': 'mean'
    }).reset_index()
    
    # Energy efficiency: generation per total consumption
    fuel_type_summary['efficiency'] = fuel_type_summary['generation'] / fuel_type_summary['total_consumption']
    
    return fuel_type_summary


# 3. Cost Analysis
def top_cost_months(df: pd.DataFrame, top_n: int = 10) -> pd.Series:
    """
    Return top N months with highest total cost.
    """
    return df.groupby('period')['cost'].sum().sort_values(ascending=False).head(top_n)

def compute_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute correlation matrix for all numeric columns.
    """
    numeric_cols = df.select_dtypes(include='number')
    return numeric_cols.corr()


if __name__ == "__main__":
    df = load_cleaned_data("C:/Users/Rylan Lewis/Desktop/USC/DSCI 510/DSCI_510_Final_Project/data/processed/cleaned_data.csv")
    print(df.describe())

    monthly_summary = compute_monthly_summary(df)
    yearly_summary = compute_yearly_summary(df)
    fuel_summary = compute_fuel_type_summary(df)
    top_months = top_cost_months(df)
    correlation = compute_correlation_matrix(df)
    
    print("Monthly Summary:")
    print(monthly_summary.head())
    print("\nYearly Summary:")
    print(yearly_summary.head())
    print("\nFuel Type Summary:")
    print(fuel_summary.head())
    print("\nTop 10 Costly Months:")
    print(top_months)
    print("\nCorrelation Matrix:")
    print(correlation)
