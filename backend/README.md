# huskyspot-backend
backend for huskyspot

## Recording Counts
A count of the number of people in each area is recorded every hour. For each feed, an single image is processed each hour using the people counting model. The model returns the number of people in each feed image and the numbers are summed to get the area count and stored into the database.

## Predictions
Predicted counts are also created hourly. For each area, the time series predictor looks at existing data up to a year and predicts up to two weeks in advance. The existing data is pulled from the database and the predicted data will be stored into the database.

## To install requirements

```bash
pip3 install -r requirements.txt
```

## To start the application

```bash
python3 app.py
```

## Endpoints

`GET /stream/<f_id>`

* Returns jpeg stream of feed
* f_id is the feed it

`GET /areas`

* Returns all areas 
```json
{"areas":[{"a_id":0,"a_name":"general_testing"}]}
```

`GET /feed/<f_id>`

* Returns information about a feed `f_id`
```json
{"a_id":0,"f_id":0,"f_name":"food_court","url":"http://32.208.120.218/mjpg/video.mjpg"}
```

`GET /area_feeds/<a_id>`

* Returns all feeds in the area `a_id`
```json
{"a_id":"0","a_name":"general_testing","count":3,"feeds":[{"f_id":0,"f_name":"food_court","url":"http://32.208.120.218/mjpg/video.mjpg"},{"f_id":1,"f_name":"laundromat","url":"http://81.14.37.24:8080/mjpg/video.mjpg"},{"f_id":2,"f_name":"shops","url":"http://87.139.9.247/mjpg/video.mjpg"},{"f_id":3,"f_name":"hair_salon","url":"http://220.240.123.205/mjpg/video.mjpg"},{"f_id":4,"f_name":"town_park","url":"http://89.29.108.38/mjpg/video.mjpg"},{"f_id":5,"f_name":"time_square","url":"http://166.130.18.45:1024/mjpg/video.mjpg"}]}
```

`GET /counts/<a_id>`
* Returns recorded counts in an area `a_id`
```json
{"a_id":"0","a_name":"general_testing","counts":[["2020-02-10 15:43:44.564039",3],["2020-02-10 15:28:44.565318",4],["2020-02-10 15:13:44.566446",5],["2020-02-10 14:58:44.567484",6],["2020-02-10 14:43:44.568558",7],["2020-02-10 14:28:44.569733",8],["2020-02-10 14:13:44.570766",9],["2020-02-10 13:58:44.571917",10],["2020-02-10 13:43:44.573030",11],["2020-02-10 13:28:44.574320",12]]}
```

`GET /predictions/<a_id>`
* Returns recorded counts in an area `a_id`
```json
{"a_id":"0","a_name":"general_testing","prediction":[["2020-02-10 16:28:44.568027",23],["2020-02-10 16:43:44.569057",24],["2020-02-10 16:58:44.570216",25],["2020-02-10 17:13:44.571315",26],["2020-02-10 17:28:44.572470",27],["2020-02-10 17:43:44.573758",28],["2020-02-10 17:58:44.574818",29]]}
```

`GET /frame/<f_id>`
* Returns a single jpeg frame from that the feed `f_id`