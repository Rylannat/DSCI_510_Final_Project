# DSCI_510_Final_Project
Project Title: How Do Heating Fuel Prices Compare Across California, and What Is Their Relationship to Energy Efficiency?

Team Members: 
  1. Abhey Sabesan Mageswaran Aryaan => USC ID: 7162-7286-71 => email: sabesanm@usc.edu
  2. Rylan Nathan Lewis => USC ID: 8358-1308-73 => email: rylannat@usc.edu

# Steps for running the Codebase:

1. Install requirements:
Install all required Python libraries using **pip install -r requirements.txt**. The project uses standard data science libraries including pandas, numpy, matplotlib, seaborn, and scikit-learn.

2. Data collection:
Raw energy data is collected from the U.S. Energy Information Administration (EIA) API using pagination and offsets to get ~28k rows of data and saved as a CSV file in the **data/raw/** directory. The data collection is done by the **get_data.py** file.

3. Data cleaning:
Run the **clean_data.py** file to remove duplicates, standardize column names and time formats, handle missing values using hierarchical imputation, and filter unnecessary fields. The cleaned dataset is saved to **data/processed/cleaned_data.csv**.

4. Run analysis:
Analysis functions are implemented in **run_analysis.py**. These functions compute time-series summaries, fuel-type statistics, efficiency metrics, and cost analyses using the cleaned dataset.

5. Visualizations:
Visualizations are generated in **visualize_results.py** by importing analysis functions from run_analysis.py. The script produces all plots used for interpretation and reporting using an interactive window. Comprehensive Inferences have been added at the bottom of this script file as comments. No jupyter notebook has been used as the script produces all the plots properly in an equivalent manner.

# Results folder:
Contains png files of each graph plotted, an inferences.txt file that has the same inferences written in visualize_results.py for easier accessibility and also the Final Project Report PDF.
