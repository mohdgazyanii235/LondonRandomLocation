from flask import Flask , render_template , send_file , request , url_for , redirect , flash , session , Markup
import random
import linecache
from flask_googlemaps import GoogleMaps
import math
import wikipedia


app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyB2gWJN7HHCh-y15I2kw1A5PqOLU22l3z8"
GoogleMaps(app)


def distance_calculator(latitude, longitude):
    min_distance = 99999999999
    min_station = ""
    with open("D:\LondonRandomLocation\AllLondonStations.csv", "r") as station_file:
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


def get_wiki(area_name):
    return wikipedia.summary(area_name, sentences=3)


@app.route('/', methods=["GET", "POST"])
def home():
    random_pcd = get_random_pcd()
    if request.method == "POST":
        random_pcd = get_random_pcd()
    random_pcd = random_pcd.split(",")
    station_name = distance_calculator(float(random_pcd[1]), float(random_pcd[2]))
    print("The closes tube station is: " + station_name)
    print(get_wiki(station_name))
    return render_template("homepage.html", random_pcd=random_pcd)


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=8000)
