from flask import Blueprint, render_template, send_file, request, make_response, jsonify, abort
from .db import get_db, close_db, get_result_set_and_count
from flask_paginate import Pagination, get_page_args
import mariadb
import folium

station = Blueprint("station", __name__)
searchcontext = "stations"

# List all stations
@station.route("/", methods=["GET"])
def stations():

    query = """SELECT SQL_CALC_FOUND_ROWS id, nimi, osoite, \
                   IF(kaupunki = ' ', 'Helsinki', kaupunki), kapasiteet FROM station LIMIT ?, ?"""

    page, per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")

    pagination_stations, station_count = get_result_set_and_count(
        offset=offset, per_page=per_page, query=query
    )

    pagination = Pagination(
        page=page, per_page=per_page, total=station_count, css_framework="bootstrap5"
    )

    return render_template(
        "stations.html",
        stationlist=pagination_stations,
        page=page,
        per_page=per_page,
        pagination=pagination,
        searchcontext=searchcontext,
    )


# Send map to the template
@station.route("/map.html")
def show_map():
    return send_file("templates/map.html")


# Single station view
@station.route("/station/<station_id>")
def station_details(station_id):

    query = """SELECT
                    nimi AS name,
                    osoite AS address,
                    if(kaupunki = ' ', 'Helsinki', kaupunki),
                    SUM(j.departure_station_id = s.id) AS departure_count,
                    SUM(j.return_station_id = s.id) AS return_count,

                    IFNULL((SELECT ROUND(avg(j.covered_distance / 1000 ), 3) 
                    FROM station s, journey j 
                    WHERE s.id =?  AND j.departure_station_id = s.id), 0) AS dep_avg_distance,
                    
                    IFNULL((SELECT ROUND(avg(j.covered_distance / 1000 ), 3) 
                    FROM station s, journey j
                    WHERE s.id =? AND j.return_station_id = s.id), 0) AS ret_avg_distance,
                    x,
                    y

                    FROM station s, journey j
                    WHERE s.id =?;"""

    try:
        cur = get_db().cursor()
        cur.execute(query, (station_id, station_id, station_id))

    except mariadb.Error as e:
        print(f"Error: {e}")
        close_db()
        return abort(500, f"Query didn't succeed.")

    for a, b, c, d, e, f, g, x, y in cur:
        name, address, kaupunki, departures, returns, dep_avg_distance, ret_avg_distance, x, y = (
            a,
            b,
            c,
            d,
            e,
            f,
            g,
            x,
            y,
        )

    map = folium.Map(location=[y, x], zoom_start=17)
    folium.Marker([y, x], popup=f"<i>{address}</i>", tooltip=name).add_to(map)
    map.save("app/templates/map.html")

    close_db()

    return render_template(
        "station.html",
        name=name,
        address=address,
        kaupunki=kaupunki,
        departures=departures,
        returns=returns,
        dep_avg_distance=dep_avg_distance,
        ret_avg_distance=ret_avg_distance,
        searchcontext=searchcontext,
    )


@station.route("/stations/search")
def stations_search():

    if request.args:
        q = request.args["q"]

        query = """SELECT SQL_CALC_FOUND_ROWS id, nimi, namn, osoite, adress, if(kaupunki = ' ', 'Helsinki', kaupunki), kapasiteet 
                FROM station 
                WHERE CONCAT( id, nimi, namn, name, osoite, adress, if(kaupunki = ' ', 'Helsinki', kaupunki), stad, operaattor, kapasiteet) 
                REGEXP ? LIMIT ?, ?"""

        page, per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")

        pagination_stations, station_count = get_result_set_and_count(
            query=query, offset=offset, per_page=per_page, phrase=q
        )

        pagination = Pagination(
            page=page, per_page=per_page, total=station_count, css_framework="bootstrap5"
        )

        return render_template(
            "stations.html",
            stationlist=pagination_stations,
            page=page,
            per_page=per_page,
            pagination=pagination,
            searchcontext=searchcontext,
        )


# Create new station
@station.route("/station/create", methods=["POST"])
def create_station():

    if request.is_json:
        req = request.get_json()

        for k, v in req.items():
            if v == None:
                res = make_response(jsonify({"message": f"No null values accepted: {k}: {v}"}), 400)
                return res

        nimi = req.get("nimi")
        namn = req.get("namn")
        name = req.get("name")
        osoite = req.get("osoite")
        adress = req.get("adress")
        kaupunki = req.get("kaupunki")
        stad = req.get("stad")
        operaattor = req.get("operaattor")
        kapasiteet = req.get("kapasiteet")
        x = req.get("x")
        y = req.get("y")

        cur = get_db().cursor()
        query = """INSERT INTO station (nimi, name, namn, osoite, adress, kaupunki, stad, operaattor, kapasiteet, x, y)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

        try:
            cur.execute(
                query,
                (nimi, name, namn, osoite, adress, kaupunki, stad, operaattor, kapasiteet, x, y),
            )
        except mariadb.Error as e:

            print(f"Error {e}")
            res = make_response(jsonify({"error": f"{e}"}), 400)
            close_db()
            return res

        # If insert succeeded
        if cur.rowcount == 1:
            response = {
                "message": "Create succesful",
                "data": {
                    "nimi": nimi,
                    "namn": namn,
                    "name": name,
                    "osoite": osoite,
                    "adress": adress,
                    "stad": stad,
                    "operaattor": operaattor,
                    "kapasiteet": kapasiteet,
                    "x": x,
                    "y": y,
                },
            }

            close_db()
            res = make_response(jsonify(response), 201)
            return res

        else:
            close_db()
            make_response(jsonify({"message:" "Create unsuccesful"}), 400)

    else:
        res = make_response(jsonify({"message": "No JSON received"}), 400)
        return res
