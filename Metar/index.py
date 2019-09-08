from flask import Flask 
from datetime import timedelta
import json
import requests
import redis




app = Flask(__name__)
r = redis.Redis(host='localhost', port=8080, db=1, password=None, socket_timeout=None)

baseurl = "https://tgftp.nws.noaa.gov/data/observations/metar/stations/"

@app.route('/metar/ping/')
def checkserver(): 
	return json.dumps({"data" :"pong"})


@app.route('/metar/<scode>/')
@app.route('/metar/<scode>/<nocache>/')
def fetchdata(scode, nocache=None): 
	if nocache == '1':
		r.setex(
				scode.upper(),
				timedelta(minutes=5),
				value=requests.get(baseurl + scode.upper() + '.TXT').text
				)

	return r.get(scode.upper()).decode('utf-8') if r.get(scode.upper()) else "Error: cache is not set/expired"