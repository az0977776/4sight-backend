import pandas as pd 
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
import matplotlib.pyplot as plt
import numpy
from datetime import datetime, timedelta

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
            print(ridx, ret.shape) # just to watch progress
        row = df.loc[ridx, :]
        for name, value in row.iteritems():
            if name not in time_conversion.keys():
                continue
            date = row["Day/Date"]
            if name == "12AM-1AM":
                # the way the census data is stored, 12-1am counts as the previous day, fixing it here
                dt = datetime.strptime(date, "%Y-%m-%d")
                dt = dt + timedelta(days=1)
                date = dt.strftime("%Y-%m-%d")
            new_row = {"ds": date + " " + time_conversion[name], "y": value}
            ret.loc[counter] = new_row
            counter += 1

    # choosing to drop all missing value rows, prophet will handle it
    ret.dropna(subset = ["y"], inplace=True)
    #ret.fillna(0)

    # sorting the values by datetime just in case, probably not needed
    ret = ret.sort_values(by=['ds'])
    ret.to_csv("reformatted.csv", sep=',', index=False)



def main():
    # how many hours to predict
    predict_hours = 24 * 14 * 1
    # for the logistic growth, capping to total people at once to 500 and min to 0
    p_cap = 500
    p_floor = 0

    df = pd.read_csv("reformatted.csv")
    df['ds'] = pd.to_datetime(df['ds'])
    df["cap"] = p_cap
    df["floor"] = p_floor

    # create the prophet model
    m = Prophet(interval_width=0.95, daily_seasonality=True, weekly_seasonality=True, yearly_seasonality='auto', changepoint_prior_scale=0.05, growth="logistic")
    m.add_country_holidays(country_name='US')

    # fit the model based on the training data
    start_date = "01-31-2018 05:00:00"
    end_date = "01-31-2019 00:00:00"
    training_mask = (df['ds'] >= start_date) & (df['ds'] < end_date)
    training_data = df.loc[training_mask]
    m.fit(training_data)

    # the actual recorded values
    start_date2 = "02-01-2019 05:00:00"
    end_date2 = "02-14-2019 00:00:00"
    actual_mask = (df['ds'] >= start_date2) & (df['ds'] < end_date2)
    actual_df = df.loc[actual_mask]

    # predicts the requested predict_hours
    future = m.make_future_dataframe(periods=predict_hours, freq='H')
    future["cap"] = p_cap
    future["floor"] = p_floor
    forecast = m.predict(future)
    forecast["yhat"] = forecast["yhat"].clip(lower=0)

    prediction = m.plot(forecast)
    components = m.plot_components(forecast)

    # comparing predicted values with actual values
    actual_mask = (forecast['ds'] >= start_date2) & (forecast['ds'] < end_date2)
    comparison = forecast.loc[actual_mask]

    # print(comparison.head())
    # print(actual_df.head())

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('time')
    ax1.set_ylabel('count')
    ax1.plot(actual_df["ds"], actual_df["y"], color=color)

    ax2 = ax1.twiny()  # instantiate a second axes that shares the same y-axis

    color = 'tab:blue'
    ax2.plot(comparison["ds"], comparison["yhat"], color=color)

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()