# Import the necessary modules
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

nba = pd.read_csv('nbaallelo_slr.csv')# Code to read in nbaallelo_slr.csv

# Perform multiple linear regression on pts, elo_i, and opp_pts
# Y = pts (response variable)
# predictor = opp_pts + elo_n

results = ols('pts ~ elo_i + opp_pts', data=nba).fit()# Code to perform multiple regression using statsmodels ols 

# Create an analysis of variance table
aov_table = sm.stats.anova_lm(results, typ=2)# Code to create ANOVA table

# Print the analysis of variance table
print(aov_table)