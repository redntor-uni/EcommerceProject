# Import the necessary modules
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols

nba = pd.read_csv('nbaallelo_slr.csv')# Code to read in nbaallelo_slr.csv

# Create a new column in the data frame that is the difference between pts and opp_pts
nba['y'] = nba['pts']-nba['opp_pts']# Code to find the difference between the columns pts and opp_pts

# Perform simple linear regression on y and elo_i
results = ols('y ~ elo_i', data=nba).fit()# Code to perform SLR using statsmodels ols 

# Create an analysis of variance table
aov_table = sm.stats.anova_lm(results, typ=2)# Code to create ANOVA table

# Print the analysis of variance table
print(aov_table)