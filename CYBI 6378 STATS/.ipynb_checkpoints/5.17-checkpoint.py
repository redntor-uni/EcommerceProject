# Import the necessary modules
import pandas as pd

nba = pd.read_csv('nbaallelo_slr.csv')# Code to read in nbaallelo_slr.csv
column_c = 'elo_i'
# Display the correlation matrix for the columns elo_i, pts, and opp_pts
columns = [column_c,'pts','opp_pts']
matrix = nba[columns].corr()
print(matrix)# Code to calculate correlation matrix

# Create a new column in the data frame that is the difference between pts and opp_pts
nba['y'] = nba['pts']-nba['opp_pts']# Code to find the difference between the columns pts and opp_pts

# Display the correlation matrix for elo_i and y
columns2 = [column_c,'y']
matrix2 = nba[columns2].corr()
print(matrix2)# Code to calculate the correlation matrix