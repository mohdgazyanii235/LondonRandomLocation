from flask import Flask , render_template , send_file , request , url_for , redirect , flash , session , Markup
import random
import linecache
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import jinja2

app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyB2gWJN7HHCh-y15I2kw1A5PqOLU22l3z8"
GoogleMaps(app)




def get_random_pcd():
    rand_line_num = random.randint(0 , 321376)
    return linecache.getline("All London PCDs.csv" , rand_line_num)


@app.route('/' , methods=["GET" , "POST"])
def home():
    random_pcd = get_random_pcd()
    if request.method == "POST":
        random_pcd = get_random_pcd()

    google_map = Map(
        identifier="view-side" ,  # for DOM element
        varname="mymap" ,  # for JS object name
        lat=37.4419 ,
        lng=-122.1419 ,
    )
    return render_template("homepage.html" , random_pcd=random_pcd, mymap=google_map)


if __name__ == '__main__':
    app.run(debug=True , host='127.0.0.1' , port=8000)
