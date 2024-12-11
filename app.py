from flask import Flask, render_template, request, Response, redirect, jsonify
from geopy.geocoders import Nominatim
import folium
import urllib.request
import os

app = Flask(__name__)

path = os.getcwd() + "/output/"

@app.route('/')
def route():
    return render_template("index.html")

@app.route('/geo')
def geo():
    return render_template("geo.html")

@app.route('/ip')
def ip():
    return render_template("ip.html")

@app.route('/id')
def id():
    return render_template("id.html")

@app.route('/envia', methods=['POST', 'GET'])
def geo_html():
    if request.method == 'POST':
        url = request.form['url']
        geolocator = Nominatim(user_agent="GetLoc")
        location = geolocator.geocode(url)
        print(location.address)
        print((location.latitude, location.longitude))

if __name__ == '__main__':
    app.run(host="localhost")