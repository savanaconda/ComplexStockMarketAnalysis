# Complex Stock Market Analysis: Time-Shifted Correlation

## Description
More complex stock market analysis to predict sector ETF performance based on past weeks' economic indicators

## Files
### Main
time-shifted_correlation.py
### Input files
Indicators_Train.csv, sector_ETFs.csv

## Implementation
This code analyzes the correlation between different economic indicators, with the goal of finding
a relationship between different indicators and stocks in order to predict the behavior of stocks
based on indicators.

Ideally, we would have an economic indicator or combination of economic indicators which correlates
with stock prices a few weeks or months in the future. This would allow us to look at the current state
of the economic indicators and buy stock which will go up in the next few weeks or months.

Therefore, this code experiments with time-shifted correlations of different indicators and stocks to
decide if there are meaningful relationships to utilize in trading algorithms.

The code can pull data from 6 sector ETFs and 20 economic indicators to visualize the relationship between
pairwise combinations of the 26 values. This code also enables time-shifting one of the values in the pair
by different time delta (i.e. test 10 day shift, 30 day shift, 100 day shift, etc.). Because all of these
combinations would result in too many plots and memory, the code is modified to only display a select few at
a time (currently it is set to look at 5 pairwise combos and 5 time deltas, resulting in 25 plots)

The plots show the relationship between the two values over time, with a line of best fit in the center. The plots
are color coordinated to show different years with different colors (2012 is red, 2013 is orange, etc.) so that it
it easier to visualize how the relationship changes over time.

Combing through the analysis, one is able to see which economic indicators act as the ideal predictors for which
stocks (sectors).

Example plots of relationships between ETFs and other ETFs and ETFs and economic indicators. Examples with varying time shifts.

## Technology vs. Basic Materials with 20 day time shift
![alt text](https://github.com/savanaconda/ComplexStockMarketAnalysis/blob/master/Technology_vs_BasicMaterials_20dayshift.png)

## Technology vs. Basic Materials with 40 day time shift
![alt text](https://github.com/savanaconda/ComplexStockMarketAnalysis/blob/master/Technology_vs_BasicMaterials_40dayshift.png)

## Technology vs. Basic Materials with 60 day time shift
![alt text](https://github.com/savanaconda/ComplexStockMarketAnalysis/blob/master/Technology_vs_BasicMaterials_60dayshift.png)

## Technology vs. Consumer Goods with 20 day time shift
![alt text](https://github.com/savanaconda/ComplexStockMarketAnalysis/blob/master/Technology_vs_ConsumerGoods_20dayshift.png)

## Technology vs. Utilities with 20 day time shift
![alt text](https://github.com/savanaconda/ComplexStockMarketAnalysis/blob/master/Technology_vs_Utilities_20dayshift.png)

## Technology vs. Unemployment Rate with 20 day time shift
![alt text](https://github.com/savanaconda/ComplexStockMarketAnalysis/blob/master/Technology_vs_UnemploymentRate_20dayshift.png)

## Technology vs. Unemployment Rate with 100 day time shift
![alt text](https://github.com/savanaconda/ComplexStockMarketAnalysis/blob/master/Technology_vs_UnemploymentRate_100dayshift.png)
