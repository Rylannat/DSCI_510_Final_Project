import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Import everything from run_analysis
from run_analysis import (
    load_cleaned_data,
    compute_monthly_summary,
    compute_yearly_summary,
    compute_fuel_type_summary,
    compute_monthly_fuel_trends,
    compute_fuel_efficiency_ranking,
    compute_fuel_cost_distribution,
    top_cost_months,
    compute_correlation_matrix,
    # compute_cost_efficiency,
    # compute_energy_per_dollar,
    # compute_emissions_proxy,
    # compute_system_efficiency_trend,
    # compute_fuel_share
)

sns.set(style="whitegrid")


# =========================================================
#  PLOT FUNCTIONS
# =========================================================

def plot_monthly_generation(monthly_summary):
    plt.figure(figsize=(12,5))
    sns.lineplot(x="period", y="generation", data=monthly_summary)
    plt.title("Monthly Total Generation Over Time")
    plt.xlabel("Month")
    plt.ylabel("Generation (MWh)")
    plt.tight_layout()
    plt.show()


def plot_monthly_cost(monthly_summary):
    plt.figure(figsize=(12,5))
    sns.lineplot(x="period", y="cost", data=monthly_summary)
    plt.title("Average Monthly Cost Over Time")
    plt.xlabel("Month")
    plt.ylabel("Cost ($)")
    plt.tight_layout()
    plt.show()


def plot_yearly_efficiency(yearly_summary):
    yearly_summary["efficiency"] = yearly_summary["generation"] / yearly_summary["total_consumption"]

    plt.figure(figsize=(10,5))
    sns.lineplot(x="year", y="efficiency", data=yearly_summary, marker="o")
    plt.title("Yearly System Efficiency (generation / total consumption)")
    plt.xlabel("Year")
    plt.ylabel("Efficiency Ratio")
    plt.tight_layout()
    plt.show()


def plot_fuel_efficiency(fuel_summary):
    plt.figure(figsize=(10,5))
    sns.barplot(
        x="fueltypedescription",
        y="efficiency",
        data=fuel_summary.sort_values("efficiency", ascending=False)
    )
    plt.title("Fuel Efficiency by Fuel Type")
    plt.xlabel("Fuel Type")
    plt.ylabel("Efficiency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_monthly_fuel_cost(monthly_fuel):
    plt.figure(figsize=(12,6))
    sns.lineplot(x="period", y="cost", hue="fueltypedescription", data=monthly_fuel)
    plt.title("Monthly Cost Trend by Fuel Type")
    plt.xlabel("Month")
    plt.ylabel("Cost")
    plt.tight_layout()
    plt.show()


def plot_cost_efficiency(cost_eff):
    plt.figure(figsize=(10,5))
    sns.barplot(
        x="fueltypedescription",
        y="cost_efficiency",
        data=cost_eff
    )
    plt.title("Cost Efficiency (Cost per BTU) — Lower is Better")
    plt.xlabel("Fuel Type")
    plt.ylabel("Cost per BTU")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_energy_per_dollar(epd):
    plt.figure(figsize=(10,5))
    sns.barplot(
        x="fueltypedescription",
        y="energy_per_dollar",
        data=epd
    )
    plt.title("Energy per Dollar (Higher = More Efficient)")
    plt.xlabel("Fuel Type")
    plt.ylabel("Energy per Dollar")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_emissions_proxy(emissions_proxy):
    plt.figure(figsize=(10,5))
    sns.barplot(
        x="fueltypedescription",
        y="emissions_proxy",
        data=emissions_proxy
    )
    plt.title("Emissions Proxy (Lower = Cleaner)")
    plt.xlabel("Fuel Type")
    plt.ylabel("Emissions Proxy")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_system_efficiency(system_eff):
    plt.figure(figsize=(10,5))
    sns.lineplot(x="year", y="efficiency", data=system_eff, marker="o")
    plt.title("System-Wide Efficiency Over Time")
    plt.xlabel("Year")
    plt.ylabel("Efficiency")
    plt.tight_layout()
    plt.show()


def plot_fuel_share(fuel_share):
    plt.figure(figsize=(12,5))
    sns.lineplot(x="year", y="share", hue="fueltypedescription", data=fuel_share)
    plt.title("Fuel Share of Total Electricity Generation Over Time")
    plt.xlabel("Year")
    plt.ylabel("Share of Total Generation")
    plt.tight_layout()
    plt.show()


def plot_top_cost_months(top_months):
    plt.figure(figsize=(12,5))
    s = top_months.sort_values(ascending=False)
    sns.barplot(x=s.index.astype(str), y=s.values)
    plt.title("Top Costliest Months")
    plt.xlabel("Month")
    plt.ylabel("Total Cost")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


def plot_correlation_matrix(corr):
    plt.figure(figsize=(12,8))
    sns.heatmap(corr, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.show()


# =========================================================
#  MAIN — RUN ANALYSIS + PLOTS
# =========================================================

if __name__ == "__main__":

    df = load_cleaned_data(
        "C:/Users/Rylan Lewis/Desktop/USC/DSCI 510/DSCI_510_Final_Project/data/processed/cleaned_data.csv"
    )

    # Run analyses
    monthly_summary = compute_monthly_summary(df)
    yearly_summary = compute_yearly_summary(df)
    fuel_summary = compute_fuel_type_summary(df)
    monthly_fuel = compute_monthly_fuel_trends(df)
    fuel_cost_dist = compute_fuel_cost_distribution(df)
    top_months_series = top_cost_months(df)
    correlation = compute_correlation_matrix(df)
    # cost_eff = compute_cost_efficiency(df)
    # epd = compute_energy_per_dollar(df)
    # emissions_proxy = compute_emissions_proxy(df)
    # system_eff = compute_system_efficiency_trend(df)
    # fuel_share = compute_fuel_share(df)

    # Generate ALL plots
    plot_monthly_generation(monthly_summary)
    plot_monthly_cost(monthly_summary)
    plot_yearly_efficiency(yearly_summary)
    plot_fuel_efficiency(fuel_summary)
    plot_monthly_fuel_cost(monthly_fuel)
    # plot_cost_efficiency(cost_eff)
    # plot_energy_per_dollar(epd)
    # plot_emissions_proxy(emissions_proxy)
    # plot_system_efficiency(system_eff)
    # plot_fuel_share(fuel_share)
    plot_top_cost_months(top_months_series)
    plot_correlation_matrix(correlation)
