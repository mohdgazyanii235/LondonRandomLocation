from flask import Flask, render_template, send_file, request, url_for, redirect, flash, session, Markup
import random
import linecache
from flask_googlemaps import GoogleMaps
import math
import wikipedia
import re


app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyB2gWJN7HHCh-y15I2kw1A5PqOLU22l3z8"
GoogleMaps(app)


def distance_calculator(latitude, longitude):
    min_distance = 99999999999
    min_station = ""
    with open("AllLondonStations.csv", "r") as station_file:
        for line in station_file:
            station_name = line.split(",")[0]
            station_lat = float(line.split(",")[1])
            station_long = float(line.split(",")[2])
            calc_distance = math.sqrt((station_lat - latitude)**2 + (station_long-longitude)**2)
            if calc_distance < min_distance:
                min_distance = calc_distance
                min_station = station_name
    return min_station


def get_random_pcd():
    rand_line_num = random.randint(0, 321376)
    return linecache.getline("All London PCDs.csv", rand_line_num)


def reformat_summary(summary):
    return re.sub("[==].*[==]", "", summary)


def get_wiki(area_name):
    try:
        return reformat_summary(wikipedia.summary(area_name, sentences=7))
    except wikipedia.exceptions.DisambiguationError as e:
        print("ran exception")
        for x in e.options:
            for y in x.split(" "):
                if y.lower() == "london":
                    return reformat_summary(wikipedia.summary(x, sentences=7))
                else:
                    return "Unfortunately we weren't able to find a description of this location"
    except wikipedia.exceptions.PageError as e:
        return "Unfortunately we weren't able to find a description of this location"


@app.route('/', methods=["GET", "POST"])
def home():
    random_pcd = get_random_pcd()
    if request.method == "POST":
        random_pcd = get_random_pcd()
    random_pcd = random_pcd.split(",")
    station_name = distance_calculator(float(random_pcd[1]), float(random_pcd[2]))

    print(station_name)
    return render_template("description_page.html", random_pcd=random_pcd, description=get_wiki(station_name),
                           station_name=station_name)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
