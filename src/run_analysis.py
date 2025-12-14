import pandas as pd


def load_cleaned_data(path: str) -> pd.DataFrame:
    """
    Load the cleaned dataset.

    """
    df = pd.read_csv(path)
    return df


# TIME-SERIES ANALYSIS
def compute_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute monthly aggregated metrics using year-month grouping.
    Ensures true monthly level and avoids duplicate '01-01' dates.

    Aggregates:
    - Sums: generation, all consumption metrics
    - Means: cost, cost_per_btu, heat_content, sulfur_content
    """
    if "year" not in df.columns:
        df["year"] = pd.to_datetime(df["period"]).dt.year
    if "month" not in df.columns:
        df["month"] = pd.to_datetime(df["period"]).dt.month

    monthly = df.groupby(["year", "month"]).agg({
        "generation": "sum",
        "total_consumption": "sum",
        "consumption_for_eg": "sum",
        "consumption_uto": "sum",
        "cost": "mean",
        "cost_per_btu": "mean",
        "heat_content": "mean",
        "sulfur_content": "mean"
    }).reset_index()

    monthly["period"] = pd.to_datetime(
        monthly[["year", "month"]].assign(day=1)
    )

    return monthly


def compute_yearly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute yearly aggregated metrics from the full dataset.
    """
    if "year" not in df.columns:
        df["year"] = pd.to_datetime(df["period"]).dt.year

    yearly = df.groupby("year").agg({
        "generation": "sum",
        "total_consumption": "sum",
        "consumption_for_eg": "sum",
        "consumption_uto": "sum",
        "cost": "mean",
        "cost_per_btu": "mean",
        "heat_content": "mean",
        "sulfur_content": "mean"
    }).reset_index()

    return yearly


# FUEL-TYPE SUMMARY ANALYSIS
def compute_fuel_type_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize metrics for each fuel type.

    Includes:
    - total generation
    - total consumption
    - mean cost & cost per BTU
    - energy efficiency (generation / total_consumption)
    """
    fuel_summary = df.groupby("fueltypedescription").agg({
        "generation": "sum",
        "total_consumption": "sum",
        "consumption_for_eg": "sum",
        "consumption_uto": "sum",
        "cost": "mean",
        "cost_per_btu": "mean"
    }).reset_index()

    fuel_summary["efficiency"] = (
        fuel_summary["generation"] / fuel_summary["total_consumption"]
    )

    return fuel_summary


# MONTHLY FUEL-TYPE TRENDS
def compute_monthly_fuel_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute monthly metrics for each fuel type.

    Useful for:
    - cost trend analysis
    - consumption patterns
    - seasonal effects
    """
    df["year"] = pd.to_datetime(df["period"]).dt.year
    df["month"] = pd.to_datetime(df["period"]).dt.month

    monthly_fuel = df.groupby(
        ["fueltypedescription", "year", "month"]
    ).agg({
        "generation": "sum",
        "total_consumption": "sum",
        "cost": "mean",
        "cost_per_btu": "mean"
    }).reset_index()

    monthly_fuel["period"] = pd.to_datetime(
        monthly_fuel[["year", "month"]].assign(day=1)
    )

    return monthly_fuel


# FUEL EFFICIENCY RANKING
def compute_fuel_efficiency_ranking(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rank fuels by pure technical efficiency:
    efficiency = generation / total_consumption
    """
    fuel_eff = df.groupby("fueltypedescription").agg({
        "generation": "sum",
        "total_consumption": "sum"
    }).reset_index()

    fuel_eff["efficiency"] = (
        fuel_eff["generation"] / fuel_eff["total_consumption"]
    )

    return fuel_eff.sort_values("efficiency", ascending=False)


# FUEL COST DISTRIBUTION
def compute_fuel_cost_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute cost distribution statistics for each fuel type.

    Provides:
    mean, median, std, min, max
    """
    return df.groupby("fueltypedescription")["cost"].agg(
        ["mean", "median", "std", "min", "max"]
    ).reset_index()


# TOP COST MONTHS
def top_cost_months(df: pd.DataFrame, top_n: int = 10) -> pd.Series:
    """
    Identify the top N most expensive months.
    """
    return df.groupby("period")["cost"].sum().sort_values(
        ascending=False
    ).head(top_n)


# CORRELATION MATRIX
def compute_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute correlations across all numeric features.
    Helps identify variables related to energy efficiency.
    """
    numeric_cols = df.select_dtypes(include="number")
    return numeric_cols.corr()

# COST EFFICIENCY BASED ON FUEL TYPE
def compute_cost_efficiency(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute cost-efficiency for each fuel type.
    Lower cost_per_btu means the fuel is cheaper per unit of energy.
    """
    ce = df.groupby("fueltypedescription")["cost_per_btu"].mean().reset_index()
    ce.rename(columns={"cost_per_btu": "cost_efficiency"}, inplace=True)
    return ce.sort_values("cost_efficiency")

# ENERGY EFFICIENCY FOR EACH FUEL
def compute_energy_per_dollar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute economic energy efficiency for each fuel:
    energy_per_dollar = total generation / total cost
    Higher values = more electricity produced per $ spent.
    """
    epd = df.groupby("fueltypedescription").agg({
        "generation": "sum",
        "cost": "mean"
    }).reset_index()

    epd["energy_per_dollar"] = epd["generation"] / epd["cost"]
    return epd.sort_values("energy_per_dollar", ascending=False)

# EMISSIONS CONTENT BY EACH FUEL
def compute_emissions_proxy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Environmental efficiency proxy:
    emissions_proxy = consumption_for_eg / generation
    Lower values = cleaner fuel (less BTU burned per kWh generated).
    """
    ep = df.groupby("fueltypedescription").agg({
        "consumption_for_eg": "sum",
        "generation": "sum"
    }).reset_index()

    ep["emissions_proxy"] = ep["consumption_for_eg"] / ep["generation"]
    return ep.sort_values("emissions_proxy")

# YEARLY SYSTEM EFFICIENCY
def compute_system_efficiency_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute yearly system-wide energy efficiency:
    efficiency_year = total_generation / total_consumption
    """
    yearly = df.groupby("year").agg({
        "generation": "sum",
        "total_consumption": "sum"
    }).reset_index()

    yearly["efficiency"] = yearly["generation"] / yearly["total_consumption"]
    return yearly

# YEARLY GENERATION SHARE FOR EACH FUEL TYPE
def compute_fuel_share(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute yearly generation share for each fuel type.
    Shows California's long-term fuel switching patterns.
    Assumes df already has a 'year' column.
    """
    gen = df.groupby(["year", "fueltypedescription"], as_index=False)["generation"].sum()

    total_per_year = gen.groupby("year")["generation"].transform("sum")

    gen["share"] = gen["generation"] / total_per_year

    return gen[["year", "fueltypedescription", "share"]]



if __name__ == "__main__":

    df = load_cleaned_data(
        "C:/Users/Rylan Lewis/Desktop/USC/DSCI 510/DSCI_510_Final_Project/data/processed/cleaned_data.csv"
    )

    print(df.describe())

    monthly_summary = compute_monthly_summary(df)
    yearly_summary = compute_yearly_summary(df)
    fuel_summary = compute_fuel_type_summary(df)
    monthly_fuel = compute_monthly_fuel_trends(df)
    fuel_eff_rank = compute_fuel_efficiency_ranking(df)
    fuel_cost_dist = compute_fuel_cost_distribution(df)
    top_months = top_cost_months(df)
    correlation = compute_correlation_matrix(df)
    cost_eff = compute_cost_efficiency(df)
    epd = compute_energy_per_dollar(df)
    emissions_proxy = compute_emissions_proxy(df)
    system_eff = compute_system_efficiency_trend(df)
    fuel_share = compute_fuel_share(df)

    print("\nMonthly Summary:")
    print(monthly_summary.head())

    print("\nYearly Summary:")
    print(yearly_summary.head())

    print("\nFuel Type Summary:")
    print(fuel_summary.head())

    print("\nMonthly Fuel Trends:")
    print(monthly_fuel.head())

    print("\nFuel Efficiency Ranking:")
    print(fuel_eff_rank)

    print("\nFuel Cost Distribution:")
    print(fuel_cost_dist)

    print("\nCost Efficiency (Lowest cost per BTU):")
    print(cost_eff)

    print("\nEnergy per Dollar (Economic Efficiency):")
    print(epd)

    print("\nEmissions Proxy (Lower = cleaner):")
    print(emissions_proxy)

    print("\nSystem-Wide Efficiency Trend:")
    print(system_eff)

    print("\nFuel Share by Year:")
    print(fuel_share)

    print("\nTop N Costly Months:")
    print(top_months)

    print("\nCorrelation Matrix:")
    print(correlation)
