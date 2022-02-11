"""
Module work with data about movies filming location
and file with map with the closest location to inputted
"""
from math import radians, sin, cos, asin, sqrt
import re
import argparse
import folium
from geopy.geocoders import Nominatim


def map_making(places, lat_1, long_1):
    """
    Function makes a map
    """
    my_map = folium.Map(location=[lat_1, long_1])
    html_close = """<h4>Location information:</h4>
     Movie title(s): {},<br>
     Address: {}
     """
    html_your = """<h3>Your place</h3>"""
    fg_loc = folium.FeatureGroup(name="Closest location")
    fg_conn = folium.FeatureGroup(name="Connections")

    repeated_place = []
    for (dist, name, place, lat, lon) in places:
        repetition = repeated_place.count([lat, lon])
        lat = lat + 0.0007*repetition
        lon = lon + 0.0007*repetition
        repeated_place.append([lat, lon])
        if dist >= 1:
            dist = str(round(dist, 1))+' km'
        else:
            dist = str(round(dist/1000)) + ' km'
        iframe = folium.IFrame(html=html_close.format(name, place),
                               width=350,
                               height=80)
        fg_loc.add_child(folium.Marker(location=[lat, lon],
                                       popup=folium.Popup(iframe),
                                       icon=folium.Icon(color="black", )))
        fg_conn.add_child(folium.PolyLine([[lat_1, long_1],
                                          [lat, lon]],
                                          tooltip=dist,
                                          weight=3,
                                          color='purple'))
    iframe = folium.IFrame(html=html_your,
                           width=105,
                           height=30)
    fg_loc.add_child(folium.Marker(location=[lat_1, long_1],
                                   popup=folium.Popup(iframe),
                                   icon=folium.Icon(color="red")))
    my_map.fit_bounds(fg_loc.get_bounds())
    my_map.add_child(fg_loc)
    my_map.add_child(fg_conn)
    my_map.add_child(folium.LayerControl())
    my_map.save('Map_film.html')


DIST_DICT = {}


def memoize(func):
    """
    Make dict with counted distance
    """
    def wrapper(*args):
        if args not in DIST_DICT:
            DIST_DICT[args] = func(*args)
        return DIST_DICT[args]
    return wrapper


@memoize
def distance_counter(place, lat_1, long_1):
    """
    The function calculates the distance
    """
    try:
        geolocator = Nominatim(user_agent="syla_liuby")
        location = geolocator.geocode(place)
        lat_2, long_2 = location.latitude, location.longitude
    except Exception:
        place_ls = place.split(", ")
        if len(place_ls) == 1:
            return -1, lat_1, long_1
        shorter_place = ", ".join(place_ls[1:])
        return distance_counter(shorter_place, lat_1, long_1)
    lon1, lat1, lon2, lat2 = map(radians, [long_1, lat_1, long_2, lat_2])
    under_sqrt = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    distance = 2 * 6371 * asin(sqrt(under_sqrt))  # Earth radius = 6371
    return distance, lat_2, long_2


def checking_location(closest_places, distance, film_name, film_place, coordinate):
    """
    Makes list with information
    of ten closest locations of filming
    """
    (latitude, longitude) = coordinate
    film_used = False
    for i, [_, fm_nm, fm_pl, _, _] in enumerate(closest_places):
        if film_place == fm_pl:
            if film_name not in fm_nm:
                fm_nm = fm_nm + ', ' + film_name
                closest_places[i][1] = fm_nm
                film_used = True
            else:
                film_used = True
    if film_used is False:
        if len(closest_places) < 10:
            closest_places.append([distance, film_name,
                                   film_place, latitude, longitude])
        else:
            max_distance = max(dist for dist in closest_places)
            if distance < max_distance[0]:
                closest_places[closest_places.index(max_distance)] = \
                    [distance, film_name, film_place, latitude, longitude]


def operate_with_data(year, lat_1, long_1, path_to_data):
    """
    Analyse every line of information and uses other functions
    """
    with open(path_to_data, 'r', encoding='UTF-8', errors='ignore') as locations:
        inf = locations.readline()
        while inf[0] != '=':
            inf = locations.readline()
        closest_places = []
        film_inf = []
        while film_inf != ['']:
            try:
                film_inf = locations.readline().split("\n")[0].split("\t")
                film_year = int(re.findall(r' \(\d\d\d\d', film_inf[0])[0][2:6])
                if film_year == year:
                    if "(" in film_inf[-1]:
                        film_inf = film_inf[:-1]
                    film_name = film_inf[0].split(str(film_year))[0][:-2]
                    film_place = film_inf[-1]
                    distance, latitude, longitude = distance_counter(film_place, lat_1, long_1)
                    if distance != -1:
                        checking_location(closest_places, distance, film_name,
                                          film_place, (latitude, longitude))
            except IndexError:
                continue
    map_making(closest_places, lat_1, long_1)


def parsing_data():
    """
    Parsing inputted data
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('year', type=int, help='year of making film')
    parser.add_argument('latitude', type=float, help='latitude of your place')
    parser.add_argument('longitude', type=float, help='longitude of your place')
    parser.add_argument('path', type=str, help='path to data file')

    args = parser.parse_args()

    year = args.year
    lat_1 = args.latitude
    long_1 = args.longitude
    path_to_data = args.path

    operate_with_data(year, lat_1, long_1, path_to_data)


if __name__ == '__main__':
    parsing_data()
