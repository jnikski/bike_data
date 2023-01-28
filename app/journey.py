from flask import Blueprint, render_template, request, make_response, jsonify
from .db import get_db, close_db, get_result_set_and_count
from flask_paginate import Pagination, get_page_args
import mariadb

journey = Blueprint("journey", __name__)


@journey.route("/journeys")
def journeys():

    query = """SELECT SQL_CALC_FOUND_ROWS 
                departure_station, 
                return_station, \
                covered_distance / 1000, \
                ROUND(duration / 60,  2) \
                FROM journey \
                ORDER BY covered_distance \
                LIMIT ?, ?"""

    page, per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")

    paginated_journeys, journey_count = get_result_set_and_count(
        offset=offset, per_page=per_page, query=query
    )

    pagination = Pagination(
        page=page, per_page=per_page, total=journey_count, css_framework="bootstrap5"
    )

    return render_template(
        "journeys.html",
        journeylist=paginated_journeys,
        page=page,
        per_page=per_page,
        pagination=pagination,
    )


@journey.route("/journeys/search")
def journeys_search():

    if request.args:
        q = request.args["q"]

        query = """SELECT SQL_CALC_FOUND_ROWS departure_station, return_station, 
                        covered_distance / 1000, 
                        ROUND(duration / 60,  2) 
                    FROM journey
                    WHERE CONCAT(departure_time, return_time, departure_station_id, departure_station,
                        return_station_id, return_station, covered_distance / 1000, ROUND(duration / 60, 2))
                    REGEXP ? LIMIT ?, ?"""

        page, per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")

        paginated_journeys, journey_count = get_result_set_and_count(
            query=query, offset=offset, per_page=per_page, phrase=q
        )
        pagination = Pagination(
            page=page,
            per_page=per_page,
            total=journey_count,
            css_framework="bootstrap5",
        )

        return render_template(
            "journeys.html",
            journeylist=paginated_journeys,
            page=page,
            per_page=per_page,
            pagination=pagination,
        )


# Create new station
@journey.route("/journey/create", methods=["POST"])
def create_journey():

    if request.is_json:
        req = request.get_json()

        for k, v in req.items():
            if v == None:
                res = make_response(jsonify({"message": f"Request had null value: {k}: {v}"}), 400)
                return res

        departure_time = req.get("departure_time")
        return_time = req.get("return_time")
        departure_station_id = req.get("departure_station_id")
        departure_station = req.get("departure_station")
        return_station_id = req.get("return_station_id")
        return_station = req.get("return_station")
        covered_distance = req.get("covered_distance")
        duration = req.get("duration")

        cur = get_db().cursor()
        query = """INSERT INTO journey (departure_time, return_time, departure_station_id, 
                    departure_station, return_station_id, return_station, covered_distance, duration)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""

        try:
            cur.execute(
                query,
                (
                    departure_time,
                    return_time,
                    departure_station_id,
                    departure_station,
                    return_station_id,
                    return_station,
                    covered_distance,
                    duration,
                ),
            )

        except mariadb.Error as e:

            print(f"Error {e}")
            close_db()
            res = make_response(jsonify({"error": f"{e}"}), 400)
            return res

        if cur.rowcount == 1:
            response = {
                "message": "Create succesful",
                "data": {
                    "departure_time": departure_time,
                    "return_time": return_time,
                    "departure_station_id": departure_station_id,
                    "departure_station": departure_station,
                    "return_station_id": return_station_id,
                    "return_station": return_station,
                    "covered_distance": covered_distance,
                    "duration": duration,
                },
            }

            close_db()
            res = make_response(jsonify(response), 201)
            return res

        else:
            close_db()
            res = make_response(jsonify({"message": "Create unsuccesful."}, 400))
            return res

    else:
        res = make_response(jsonify({"message": "No valid JSON received"}), 400)
        return res
