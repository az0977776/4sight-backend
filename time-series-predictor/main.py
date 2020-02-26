import pandas as pd 
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
import matplotlib.pyplot as plt
import numpy

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

    #ret.dropna(subset = ["y"], inplace=True)
    ret.fillna(0)
    ret.to_csv("reformatted.csv", sep=',', index=False)

def main():
    # how many hours to predict
    predict_hours = 24 * 7 * 1

    df = pd.read_csv("reformatted.csv")
    df['ds'] = pd.to_datetime(df['ds'])
        
    # create the prophet model
    m = Prophet(daily_seasonality=True, weekly_seasonality=True, yearly_seasonality='auto')
    # m.add_country_holidays(country_name='US')

    # fit the model based on the training data
    start_date = "01-23-2018"
    end_date = "02-23-2018"
    training_mask = (df['ds'] > start_date) & (df['ds'] <= end_date)
    training_data = df.loc[training_mask]
    m.fit(training_data)

    # the actual recorded values
    # start_date2 = "01-22-2019"
    # end_date2 = "01-24-2019"
    # actual_mask = (df['ds'] > start_date2) & (df['ds'] <= end_date2)
    # actual_df = df.loc[actual_mask]

    # predicts the requested predict_hours
    future = m.make_future_dataframe(periods=predict_hours, freq='H')
    forecast = m.predict(future)

    prediction = m.plot(forecast)
    # a = add_changepoints_to_plot(prediction.gca(), m, forecast)
    components = m.plot_components(forecast)
    plt.show()

    # look at predicted values with actual values
    # forecast["y_actual"] = actual_df["y"]
    # comparison = forecast.loc[actual_mask]
    # tmp = comparison[['ds','yhat','y_actual']]

    # plt.figure()
    # plt.plot(comparison["ds"], comparison["yhat"], 'b', comparison["ds"], comparison["y_actual"], 'g')
    # plt.show()

if __name__ == "__main__":
    main()