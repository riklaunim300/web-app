from flask import Flask, json, render_template, request, Response, redirect, jsonify
from geopy.geocoders import Nominatim
import folium
import urllib.request
import os
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from opencage.geocoder import OpenCageGeocode

key = '29863443ad13421181f0d61b9900932e'

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
        m = folium.Map(location=[location.latitude, location.longitude], zoom_start=10)
        m.save(path + 'location.html')
        with open(path + 'location.html', "r") as file:
            content = file.read()
            return Response(content, mimetype='text/html')

@app.route('/envia2', methods=['POST', 'GET'])
def ip_html():
    if request.method == 'POST':
        ip = request.form['url']
        url = urllib.request.urlopen("https://geolocation-db.com/jsonp/" + ip)
        data = url.read().decode()
        data = data.split("(")[1].strip(")")
        parsed = json.loads(data)
        parsed_2 = json.dumps(parsed, indent=4, sort_keys=True)
        print(parsed_2)
        return render_template('out.html', temp=parsed_2)
    
@app.route('/envia3', methods=['POST', 'GET'])
def id_html():
    if request.method == 'POST':
        mobile = request.form['url']
        mobile = phonenumbers.parse(mobile)
        geocoder2 = OpenCageGeocode(key)
        query = str(mobile)
        result = geocoder2.geocode(query)
        a = timezone.time_zones_for_number(mobile)
        b = carrier.name_for_number(mobile, "en")
        c = geocoder.description_for_number(mobile, "en")
        d = phonenumbers.is_valid_number(mobile)
        e = phonenumbers.is_possible_number(mobile)
        print(result)
        print(a)
        print(b)
        print(c)
        print("Valid mobile Number: ", d)
        print("Checking possibity Number: ", e)
        result_1 = "Town: " + f"{a}" + "," +"Carrier: " + f"{b}" + "," + "Country: " + f"{c}" + "," + "Geolocation: " + f"{result}" + "," + "Valid mobile Number: " + f"{d}" + "," + "Checking possibity Number: " + f"{e}"
        return render_template('out.html', temp=result_1)

if __name__ == '__main__':
    app.run(host="localhost")