# This code analyzes the correlation between different economic indicators, with the goal of finding
# a relationship between different indicators and stocks in order to predict the behavior of stocks
# based on indicators.
#
# Ideally, we would have an economic indictor or combination of economic indicators which correlates
# with stock prices a few weeks or months in the future. This would allow us to look at the current state
# of the economic indicators and buy stock which will go up in the next few weeks or months.
#
# Therefore, this code experiments with time-shifted correlations of different indicators and stocks to
# decide if there are meaningful relationships to utilize in trading algorithms.
#
# The code can pull data from 6 sector ETFs and 20 economic indicators to visualize the relationship between
# pairwise combinations of the 26 values. This code also enables time-shifting one of the values in the pair
# by different time delta (i.e. test 10 day shift, 30 day shift, 100 day shift, etc.). Because all of these
# combinations would result in too many plots and memory, the code is modified to only display a select few at
# a time (currently it is set to look at 5 pairwise combos and 5 time deltas, resulting in 25 plots)
#
# The plots show the relationship between the two values over time, with a line of best fit in the center. The plots
# are color coordinated to show different years with different colors (2012 is red, 2013 is orange, etc.) so that it
# it easier to visualize how the relationship changes over time.
#
# Combing through the analysis, one is able to see which economic indicators act as the ideal predictors for which
# stocks (sectors)



import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import itertools as it
import re
from scipy import stats



plot_figures = True

#-------------------------------------------------------------------------------------------------#
#---------------------------------------Sub Functions---------------------------------------------#
#-------------------------------------------------------------------------------------------------#

def get_predictors(combo, days_shifted):
	# The way that the combos are structured, the first one is going to be the one we want to predict (the ETF) and the
	# second one is going to be the one we want to make the prediction based on -- in the linear regression, x and y are
	# switched to account for this
	x1 = combo[0]
	y1 = combo[1]
	x = combo_df[x1]
	y = combo_df[y1]

	slope, intercept, r_value, p_value, std_err = stats.linregress(y[days_shifted:], x[:-days_shifted])
	label = (x1 + ' vs ' + y1)

	return label, slope, intercept


def get_prediction_and_plot(combo, days_shifted, plot_figures):
	x1 = combo[0]
	y1 = combo[1]
	x = combo_df[x1]
	y = combo_df[y1]

	corr = np.corrcoef(x[days_shifted:], y[:-days_shifted])

	slope, intercept, r_value, p_value, std_err = stats.linregress(x[days_shifted:], y[:-days_shifted])
	# print("Slope: %f \n Intercept: %f \n r_value: %f \n p_value: %f \n std_err: %f" % (slope, intercept, r_value, p_value, std_err))
	predicted_y = intercept + slope*x

	# Figures:
	if plot_figures== True:
		plt.figure()
		plt.plot(x[start_date:seg1], y[start_date:seg1], 'tab:red' ,marker ='o', markersize=4, linestyle='None')
		plt.plot(x[seg1:seg2], y[seg1:seg2], 'tab:orange' ,marker ='o', markersize=4, linestyle='None')
		plt.plot(x[seg2:seg3], y[seg2:seg3], 'tab:green' ,marker ='o', markersize=4, linestyle='None')
		plt.plot(x[seg3:seg4], y[seg3:seg4], 'tab:cyan' ,marker ='o', markersize=4, linestyle='None')
		plt.plot(x[seg4:seg5], y[seg4:seg5], 'tab:blue' ,marker ='o', markersize=4, linestyle='None')
		plt.plot(x[seg5:end_date], y[seg5:end_date], 'tab:purple' ,marker ='o', markersize=4, linestyle='None')
		plt.plot(x, predicted_y, 'k', label = 'Line of best fit')
		plt.xlabel(x1)
		plt.ylabel(y1 + ' shifted ' + str(days_shifted) + ' days ')
		plt.title('Correlation coefficient: '+ str(corr[0][1]) + '    Days Shifted of Y-axis: '+ str(days_shifted))
		plt.legend([start_date + ' to ' + seg1, seg1 + ' to ' + seg2, seg2 + ' to ' + seg3, seg3 + ' to ' + seg4, seg4 + ' to ' + seg5, seg5 + ' to ' + end_date])

	corr_coefs.append(str(corr[0][1]))
	labels.append(x1 + ' vs ' + y1)

	return labels, corr_coefs






#-------------------------------------------------------------------------------------------------#
#------------------------------------MAIN STARTS HERE---------------------------------------------#
#-------------------------------------------------------------------------------------------------#

# Date selection
start_date = '20120309' #This is the furthest back data for which we have all the economic indicators
end_date = '20180101'

# highs = pd.read_csv('stocks-us-adjHigh.csv', parse_dates=True, index_col=0)
# opens = pd.read_csv('stocks-us-adjOpen.csv', parse_dates=True, index_col=0)
# closes = pd.read_csv('stocks-us-adjClose.csv', parse_dates=True, index_col=0)
# lows = pd.read_csv('stocks-us-adjLow.csv', parse_dates=True, index_col=0)
# volumes = pd.read_csv('stocks-us-Volume.csv', parse_dates=True, index_col=0)

parser_ind = lambda date: pd.to_datetime(date, format='%m/%d/%Y')
indicators = pd.read_csv('Indicators_Train.csv', parse_dates=True, date_parser=parser_ind, index_col=0, skiprows=[1])
sector_ETFs = pd.read_csv('sector_ETFs.csv', parse_dates=True, date_parser=parser_ind, index_col=0)

# Get custom dates for data set
# highs = highs.loc[start_date:end_date]
# opens = opens.loc[start_date:end_date]
# closes = closes.loc[start_date:end_date]
# lows = lows.loc[start_date:end_date]
# volumes = volumes.loc[start_date:end_date]

indicators = indicators.loc[start_date:end_date]
sector_ETFs = sector_ETFs.loc[start_date:end_date]


#Resample data
resample = False

if resample == True:
	indicators_resampled = indicators.resample('M').first()
	sector_ETFs_resampled = sector_ETFs.resample('M').first()
	indicators = indicators_resampled
	sector_ETFs = sector_ETFs_resampled


# Remove dt columns
for column in indicators.columns.values:
	m = re.match('([0-9a-zA-Z]+)(_dt)',column)
	if m:
		indicators.drop(m.group(0), axis=1,inplace=True)


seg1 = '20130101'
seg2 = '20140101'
seg3 = '20150101'
seg4 = '20160101'
seg5 = '20170101'


list_ETFs = list(sector_ETFs.columns.values)
combos_ETFs = list(it.combinations(list_ETFs,2))
list_indicators = list(indicators.columns.values)
combos_indicators = list(it.combinations(list_indicators,2))
list_both = list_ETFs + list_indicators
combos = list(it.combinations(list_both,2))

# Limit the number of combos to look at a subset and not overwhelm python
combos = combos[0:5]
print(combos)

combo_df = indicators.join(sector_ETFs,how='inner')


# combos = combos[0:13]

# combo_df = sector_ETFs
# combos = combos_ETFs




#Create array of the different days shifted we want to test out
days_shifted_array = []
i = 20
while i <= 100:
	days_shifted_array.append(i)
	i = i + 20
#


#Plot each sector combo to see the correlation coefficients between the two
headers = ['Sector Combos']
all_corr_coefs = []
all_predictors = []

for idx, days_shifted in enumerate(days_shifted_array):
	print(idx)
	corr_coefs = []
	labels = []
	for combo in combos:
		labels, corr_coefs = get_prediction_and_plot(combo, days_shifted, plot_figures)
		label, slope, intercept = get_predictors(combo, days_shifted)
		all_predictors.append([label, str(days_shifted), slope, intercept])
	all_corr_coefs.append(corr_coefs)
	headers.append(str(days_shifted) + ' days shifted')

all_predictors_df = pd.DataFrame(all_predictors,columns=['combo', 'days shifted', 'slope', 'intercept'])

# print(all_predictors_df.head())

#


# Process correlation coefficients to write to CSV
all_corr_coefs_df = pd.DataFrame(all_corr_coefs)

data = all_corr_coefs_df.transpose()

data.insert(loc=0, column='labels', value=labels)
data.columns = headers

data.to_csv('Corr_Coefficients_overtime.csv', index = False)
#


# Determine the highest correlation coefficients for each sector, looking at
# all of the sector + days shifted combos for the most correlated
data.set_index('Sector Combos', inplace=True)
highestcorr_combos = []
highestdays_shifted = []

indic_forpredict = []
for ETF in list_ETFs:
	ETF_indexes = []
	ETF_only = pd.DataFrame()
	for value in data.index.values:	
		# Match the ETF in question
		regex = re.escape(ETF) + ' vs [A-Z][A-Z]+'
		m = re.search(regex, value)
		if m:
			ETF_indexes.append(value)
			ETF_only = ETF_only.append(data.loc[value])
	


	# max_index_x = ETF_only.max(axis=0).idxmax()
	# max_index_y = ETF_only.max(axis=1).idxmax()


	# highestcorr_combos.append(max_index_y)
	# m = re.match('([0-9]+)( days shifted)',max_index_x)
	# if m:
	# 	days = m.group(1)
	# 	highestdays_shifted.append(days)

	# # print(max_index_y)

	# # Match which indicator is used to predict it
	# n = re.match(' ([A-Z][A-Z]+)',max_index_y)
	# if n:
	# 	indic = n.group(0)
	# 	indic_forpredict = indic_forpredict.append(indic)

		# print(indic)


	# predictor_line = all_predictors_df.loc[(all_predictors_df['combo'] == max_index_y) & (all_predictors_df['days shifted'] == days)]
	# x = sector_ETFs[ETF]
	# intercept = predictor_line['intercept'].values[0]
	# slope = predictor_line['slope'].values[0]
	# predicted_y = intercept + slope*x
	# actual_y = x

	# test = 1
	# if test == 0:
	# 	plt.figure()
	# 	plotTitle = str(ETF)
	# 	predicted_y.plot()
	# 	actual_y.plot()
	# 	plt.title(plotTitle)
	# 	plt.xlabel('Time')
	# 	plt.ylabel('Predicted ETF Price')
		# dates = pd.date_range(start=start_date, end=end_date)
		# plt.plot_date(dates, predicted_y)
		# print(sector_ETFs)

# print(highestcorr_combos)
# print(highestdays_shifted)

	# 
#


# NEED TO GET THE PREDICT Y OUT OF THE DATA-- predicted y variables from before, then just index them with the indexes found in the for loop above
# print(data.head())

# Plot highest correlated combos and get the predictions
# for combo, days_shifted in zip(highestcorr_combos,highestdays_shifted):
	#nothing

if plot_figures == True:
	plt.show()