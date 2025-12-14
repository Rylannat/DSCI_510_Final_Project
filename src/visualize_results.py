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
    compute_cost_efficiency,
    compute_energy_per_dollar,
    compute_emissions_proxy,
    compute_system_efficiency_trend,
    compute_fuel_share
)

sns.set(style="whitegrid")


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


if __name__ == "__main__":

    df = load_cleaned_data(
        "../data/processed/cleaned_data.csv"
    )

    monthly_summary = compute_monthly_summary(df)
    yearly_summary = compute_yearly_summary(df)
    fuel_summary = compute_fuel_type_summary(df)
    monthly_fuel = compute_monthly_fuel_trends(df)
    fuel_cost_dist = compute_fuel_cost_distribution(df)
    top_months_series = top_cost_months(df)
    correlation = compute_correlation_matrix(df)
    cost_eff = compute_cost_efficiency(df)
    epd = compute_energy_per_dollar(df)
    emissions_proxy = compute_emissions_proxy(df)
    system_eff = compute_system_efficiency_trend(df)
    fuel_share = compute_fuel_share(df)

    plot_monthly_generation(monthly_summary)
    plot_monthly_cost(monthly_summary)
    plot_yearly_efficiency(yearly_summary)
    plot_fuel_efficiency(fuel_summary)
    plot_monthly_fuel_cost(monthly_fuel)
    plot_cost_efficiency(cost_eff)
    plot_energy_per_dollar(epd)
    plot_emissions_proxy(emissions_proxy)
    plot_system_efficiency(system_eff)
    plot_fuel_share(fuel_share)
    plot_top_cost_months(top_months_series)
    plot_correlation_matrix(correlation)



"""
INFERENCE:

1. Monthly Total Generation Over Time:
The total monthly generation is gradually increasing from 2020 until the end of 2024, which is a clear indication 
of the overall steady growth in electricity output. In 2025, the generation decreases drastically which could mean 
that either the data for the year is incomplete or there has been a major change in the system.

2. Correlation Heatmap:
Generation has very strong positive correlations with total consumption and other related consumption metrics, thus 
confirming that a higher fuel usage leads almost linearly to increased electricity output. The cost and cost_per_btu 
are significantly correlated with heat_content and sulfur_content which means that the quality and the composition of 
the fuel influence the pricing.

3. Top Costliest Months:
The first single most expensive month shows a total cost that is substantially higher than all the other months combined, 
thus making it a clear cost outlier that needs to be investigated further (e.g. fuel price spikes or demand shocks). 
Several of the rest of the costliest months are clustered around the years 2022-2023, thus going hand in hand with the 
broader upward cost trends that are also present in other plots.

4. System-Wide Efficiency Over Time:
System-wide efficiency keeps on getting better from 2020 until 2024 which is a sign that the conversion of fuel 
consumption into electricity gets more and more efficient over time. In 2025 the efficiency is declining, this could 
be a reflection of operational changes, fuel mix shifts or even partial-year data.

5: Monthly Cost Trend by Fuel Type:
Most visible cost changes are influenced by a handful of fuels whose costs rise from 2020 to a peak somewhere around 
2022-2023 and then become moderate again in 2024. A lot of fuel types are close to zero in terms of the plotted cost 
scale which could mean that they are being used minimally or their cost contributions are relatively insignificant as 
compared to the main fuels.

6. Emissions Proxy by Fuel:
The fuels that have the lowest emissions proxy values can be considered the cleanest ones in this dataset as they are 
using less BTUs per unit of generation. There are several fuel sources that have significantly higher emissions proxies,
thus indicating that they should be the first ones to be replaced in any decarbonization strategy.

7. Yearly System Efficiency (generation / total consumption):
The annual efficiency ratio is very similar to the system-wide efficiency one showing the system's trend of increasing 
electricity production per unit of fuel consumed up to 2024. The reason for the drop in 2025 could be either an 
efficiency issue that is coming up or that the data for the year is not complete as compared to the previous ones.

8. Fuel Efficiency by Fuel Type:
There are only a few fuel types that can boast of much higher technical efficiency (generation/consumption) than the 
others, in this way, they become the outstanding performers from an energy-conversion point of view alone. There are 
some fuels that are concentrated at low or even close to zero efficiency which means that these are either measurement 
anomalies or conversion performance is extremely unfavorable.

9. Average Monthly Cost Over Time:
The average monthly cost starts at 2020 and gradually increases until it reaches a peak around 2022, thus reflecting 
the escalation of expenditures per month during that time. In 2023-2024, expenses are toned down but still remain 
higher than those at the beginning of the period and then there is a slight upward trend again in 2025, thus indicating 
a kind of new equilibrium at a higher cost level.

10. Cost Efficiency per BTU:
Looking at the cost per BTU of the different fuels, one can see that natural gas along with other related gas categories
have relatively low costs per BTU which makes them economically advantageous energy sources. There are some fuels that 
have considerably higher costs per BTU which makes them less attractive from a cost-efficiency standpoint even without 
considering emissions.

11. Energy per Dollar per Fuel:
There is a handful of fuels that provides tremendously high energy per dollar, thus pointing out the strong economic 
efficiency when both one generation and one cost are considered jointly. On the other hand, there are a lot of fuels 
that offer relatively low energy per dollar, thus indicating that these are more expensive options once they are 
normalized by delivered electricity.

"""