# huskyspot-backend
backend for huskyspot

## To install requirements

```bash
pip3 install -r requirements.txt
```

## To start the application

```bash
python3 app.py
```

## Endpoints

`GET /feed?<f_id>`

* Returns jpeg stream of feed
* f_id is the feed it

`GET /areas`

* Returns all areas 
```json
{"areas":[{"a_id":0,"name":"general_testing"}]}
```

`GET /feeds/<a_id>`

* Returns all feeds in the area `a_id`
```json
{"feeds":
[{"a_id":0,"f_id":0,"name":"food_court","url":"http://32.208.120.218/mjpg/video.mjpg"},{"a_id":0,"f_id":1,"name":"laundromat","url":"http://81.14.37.24:8080/mjpg/video.mjpg"},{"a_id":0,"f_id":2,"name":"shops","url":"http://87.139.9.247/mjpg/video.mjpg"},{"a_id":0,"f_id":3,"name":"hair_salon","url":"http://220.240.123.205/mjpg/video.mjpg"},{"a_id":0,"f_id":4,"name":"town_park","url":"http://89.29.108.38/mjpg/video.mjpg"},{"a_id":0,"f_id":5,"name":"time_square","url":"http://166.130.18.45:1024/mjpg/video.mjpg"}]}
```

`GET /counts/<f_id>`
* Returns recorded counts in a feed `f_id`
```json
{"counts":[["2020-02-05 14:57:07.507277",3],["2020-02-05 14:42:07.508417",4],["2020-02-05 14:27:07.509579",5],["2020-02-05 14:12:07.510923",6],["2020-02-05 13:57:07.511990",7],["2020-02-05 13:42:07.513068",8],["2020-02-05 13:27:07.514220",9],["2020-02-05 13:12:07.515403",10],["2020-02-05 12:57:07.516595",11],["2020-02-05 12:42:07.517738",12]],"f_id":"3"}
```

`GET /predictions/<f_id>`
* Returns recorded counts in a feed `f_id`
```json
{"f_id":"3","prediction":[["2020-02-05 15:27:07.510351",22],["2020-02-05 15:42:07.511472",23],["2020-02-05 15:57:07.512563",24],["2020-02-05 16:12:07.513607",25],["2020-02-05 16:27:07.514844",26],["2020-02-05 16:42:07.515965",27],["2020-02-05 16:57:07.517219",28],["2020-02-05 17:12:07.518239",29]]}
```