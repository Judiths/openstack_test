from __future__ import print_function
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot

import data
import chk
import string

#dta, x = data.dataHandler('./tmpfile00431',0.5)
def arima_handler(dta, start, end):
    #dta, x = data.dataHandler('./tmpfile00431',0.5)
    dta = pd.TimeSeries(dta)
    #dta.index = pd.Index(sm.tsa.datetools.dates_from_range('1700','2060'))
    dta.index = pd.Index(sm.tsa.datetools.dates_from_range(start,end))
    dta.plot(figsize=(12,8))

    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(dta.values.squeeze(), lags=40, ax=ax1)
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(dta, lags=40, ax=ax2)

    arma_mod20 = sm.tsa.ARMA(dta, (2,0)).fit()
    #print(arma_mod20)

    arma_mod30 = sm.tsa.ARMA(dta, (3,0)).fit()
    #print(arma_mod30)

    print(arma_mod20.aic, arma_mod20.bic, arma_mod20.hqic)
    print(arma_mod30.aic, arma_mod30.bic, arma_mod30.hqic)

    if arma_mod20.aic < arma_mod30.aic:
        sm.stats.durbin_watson(arma_mod20.resid.values)
        fig = plt.figure(figsize=(12,8))
        ax = fig.add_subplot(111)
        ax = arma_mod20.resid.plot(ax=ax);

        resid = arma_mod20.resid
        stats.normaltest(resid)

        fig = plt.figure(figsize=(12,8))
        ax = fig.add_subplot(111)
        fig = qqplot(resid, line='q', ax=ax, fit=True)

        fig = plt.figure(figsize=(12,8))
        ax1 = fig.add_subplot(211)
        fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=40, ax=ax1)
        ax2 = fig.add_subplot(212)
        fig = sm.graphics.tsa.plot_pacf(resid, lags=40, ax=ax2)

        r,q,p = sm.tsa.acf(resid.values.squeeze(), qstat=True)
        data = np.c_[range(1,41), r[1:], q, p]
        #table = pandas.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
        table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
        #print(table.set_index('lag'))

        predict_sunspots = arma_mod20.predict(str(string.atoi(start)+360),str(string.atoi(end)+5), dynamic=True)
        #print(predict_sunspots)
        return predict_sunspots

        #ax = dta.ix['1700':].plot(figsize=(12,8))
        #ax = predict_sunspots.plot(ax=ax,style='r--',abel='Dyn Prediction');
        #ax.legend();

        #chk.mean_forecast_err(dta.None, predict_sunspots)

