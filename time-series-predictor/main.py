import pandas as pd 
from fbprophet import Prophet
import matplotlib
import numpy


def main():
    df = pd.read_csv("reformatted.csv")
    df = df.loc[:1 * 28 * 24, :]
    m = Prophet(changepoint_prior_scale=0.01)
    m.add_country_holidays(country_name='US')
    # m.add_seasonality(name='daily', period=1, fourier_order=20)
    # m.add_seasonality(name='monthly', period=30, fourier_order=5)
    m.fit(df)

    future = m.make_future_dataframe(periods=24 * 7, freq='H')
    forecast = m.predict(future)
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
    fig1 = m.plot(forecast)
    fig2 = m.plot_components(forecast)
    matplotlib.pyplot.show(fig1) 
    matplotlib.pyplot.show(fig2) 
    

time_conversion = {
    "5AM-6AM": "05:00:00",
    "6AM-7AM": "06:00:00",
    "7AM-8AM": "07:00:00",
    "8AM-9AM": "08:00:00",
    "9AM-10AM": "09:00:00",
    "10AM-11AM": "10:00:00",
    "11AM-12PM": "11:00:00",
    "12PM-1PM": "12:00:00",
    "1PM-2PM": "13:00:00",
    "2PM-3PM": "14:00:00",
    "3PM-4PM": "15:00:00",
    "4PM-5PM": "16:00:00",
    "5PM-6PM": "17:00:00",
    "6PM-7PM": "18:00:00",
    "7PM-8PM": "19:00:00",
    "8PM-9PM": "20:00:00",
    "9PM-10PM": "21:00:00",
    "10PM-11PM": "22:00:00",
    "11PM-12AM": "23:00:00",
    "12AM-1AM": "00:00:00"
}
    
def reformat_data():
    df = pd.read_csv("marino_census.csv")
    ret = pd.DataFrame(columns=["ds", "y"])
    counter = 0

    for ridx in range(df.shape[0]):
        if ridx % 50 == 0:
            print(ridx, ret.shape)
        row = df.loc[ridx, :]
        for name, value in row.iteritems():
            if name not in time_conversion.keys():
                continue
            new_row = {"ds": row["Day/Date"] + " " + time_conversion[name], "y": value}
            ret.loc[counter] = new_row
            counter += 1

    ret.dropna(subset = ["y"], inplace=True)
    print(ret)
    ret.to_csv("reformatted.csv", sep=',')

if __name__ == "__main__":
    main()