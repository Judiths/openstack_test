def mean_forecast_err(y, yhat):
    return y.sub(yhat).mean()
