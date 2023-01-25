from flask import Blueprint, render_template, request
from .db import  get_db, close_db, get_result_set_and_count
from flask_paginate import Pagination, get_page_args
import mariadb

station = Blueprint('station', __name__)


# List all stations
@station.route("/", methods=["GET"])
def stations():

    query = """SELECT SQL_CALC_FOUND_ROWS id, nimi, namn, osoite, \
                   adress, kaupunki, kapasiteet FROM station LIMIT ?, ?"""

    page, per_page, offset = get_page_args(
        page_parameter="page",  per_page_parameter="per_page")

    pagination_stations, station_count = get_result_set_and_count(
        offset=offset, per_page=per_page, query=query)

    pagination = Pagination(page=page, per_page=per_page,
                            total=station_count, css_framework="bootstrap5")

    return render_template("stations.html", stationlist=pagination_stations, page=page, per_page=per_page, pagination=pagination)


# Single station view
@station.route("/station/<station_id>")
def station_details(station_id):
    try:
        cur = get_db()

        cur.execute("""SELECT
                    nimi AS name,
                    osoite AS address,
                    SUM(j.departure_station_id = s.id) AS departure_count,
                    SUM(j.return_station_id = s.id) AS return_count,
                    (SELECT round(avg(j.covered_distance / 1000 ), 3) 
                    FROM station s, journey j 
                    WHERE s.id =?  and j.departure_station_id = s.id) AS dep_avg_distance,
                    (SELECT round(avg(j.covered_distance / 1000 ), 3) 
                    FROM station s, journey j
                    where s.id =? and j.return_station_id = s.id) AS ret_avg_distance
                    from station s, journey j
                    WHERE s.id =?;""", (station_id, station_id, station_id,))

    except mariadb.Error as e:
        print(f"Error: {e}")

    for a, b, c, d, e, f in cur:
        name, address, departures, returns, dep_avg_distance, ret_avg_distance = a, b, c, d, e, f

    close_db()

    return render_template("station.html", name=name, address=address, departures=departures, returns=returns, dep_avg_distance=dep_avg_distance, ret_avg_distance=ret_avg_distance)


@station.route('/stations/search')
def stations_search():

    if request.args:
        q = request.args['q']

        query = """SELECT SQL_CALC_FOUND_ROWS id, nimi, namn, osoite, adress, kaupunki, kapasiteet 
                FROM station 
                WHERE CONCAT( id, nimi, namn, name, osoite, adress, kaupunki, stad, operaattor, kapasiteet) 
                REGEXP ? LIMIT ?, ?"""

        page, per_page, offset = get_page_args(
            page_parameter="page",  per_page_parameter="per_page")

        pagination_stations, station_count = get_result_set_and_count(
            query=query, offset=offset, per_page=per_page, phrase=q)
        # print(f'station_count: {station_count}')
        pagination = Pagination(page=page, per_page=per_page,
                                total=station_count, css_framework="bootstrap5")

        return render_template("stations.html", stationlist=pagination_stations, page=page, per_page=per_page, pagination=pagination)
