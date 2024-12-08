import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as sms

internet = pd.read_csv('internetusage.csv')# load the file internetusage.csv
keep = ['State','internet_usage','bachelors_degree']
internet = internet[keep]
model = sms.ols('internet_usage ~ bachelors_degree', data=internet).fit() # fit a linear model using the sms.ols function and the internet dataframe

bach_percent = float(input())

prediction = model.predict(pd.Series([1,bach_percent]),transform=False)# use the model.predict function to find the predicted value for internet_usage using 
prediction = prediction.reset_index(drop=True)
print(prediction)
# print(formula_result)
