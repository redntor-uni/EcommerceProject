# Import the necessary modules
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

nba = pd.read_csv('nbaallelo_mlr.csv')# Code to read in nbaallelo_mlr.csv
#pts is response/Y variable
#elo_i, game_result_W, and opp_pts are predictiable variables

# Recode the column game_result into a dummy variable, game_result, with W = 1 and L = 0
nba = nba.replace('L', 0)
nba = nba.replace('W',1)
nba = nba.rename(columns={'game_result':'game_result_W'})

results = ols('pts ~ elo_i + game_result_W + opp_pts', data=nba).fit()# Code to perform multiple regression using statsmodels ols 

# Create an analysis of variance table
aov_table = sm.stats.anova_lm(results, typ=2)# Code to create ANOVA table

# Print the analysis of variance table
print(aov_table)