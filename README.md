# DSCI_510_Final_Project
Project Title: How Do Heating Fuel Prices Compare Across California, and What Is Their Relationship to Energy Efficiency?
Team Members: 
  1. Abhey Sabesan Mageswaran Aryaan:

Install requirements:
Install all required Python libraries using pip install -r requirements.txt. The project uses standard data science libraries including pandas, numpy, matplotlib, seaborn, and scikit-learn.

Data collection:
Raw energy data is collected from the U.S. Energy Information Administration (EIA) API and saved as a CSV file in the data/raw/ directory.

Data cleaning:
Run the data cleaning script to remove duplicates, standardize column names and time formats, handle missing values using hierarchical imputation, and filter unnecessary fields. The cleaned dataset is saved to data/processed/cleaned_data.csv.

Run analysis:
Analysis functions are implemented in src/run_analysis.py. These functions compute time-series summaries, fuel-type statistics, efficiency metrics, and cost analyses using the cleaned dataset.

Produce visualizations:
Visualizations are generated in a Jupyter notebook (.ipynb) by importing analysis functions from run_analysis.py. The notebook produces all plots used for interpretation and reporting.
