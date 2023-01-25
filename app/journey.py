from flask import Blueprint, render_template, request
from .db import get_result_set_and_count
from flask_paginate import Pagination, get_page_args

journey = Blueprint('journey', __name__)


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

    page, per_page, offset = get_page_args(
    page_parameter="page",  per_page_parameter="per_page")

    print(f' page: {page}, per_page: {per_page}, offset: {offset}')
    paginated_journeys, journey_count = get_result_set_and_count(offset=offset, per_page=per_page, query=query)
    pagination = Pagination(page=page, per_page=per_page,
                            total=journey_count, css_framework="bootstrap5")

    print(paginated_journeys)
    print(paginated_journeys[0])
    print(paginated_journeys[0][0])
    return render_template("journeys.html", journeylist=paginated_journeys, page=page, per_page=per_page, pagination=pagination)


@journey.route('/journeys/search')
def journeys_search():
    
    if request.args:
        q = request.args['q']
     
        query = """SELECT SQL_CALC_FOUND_ROWS departure_station, return_station, 
                        covered_distance / 1000, 
                        ROUND(duration / 60,  2) 
                    FROM journey
                    WHERE CONCAT(departure_time, return_time, departure_station_id, departure_station,
                        return_station_id, return_station, covered_distance / 1000, ROUND(duration / 60, 2))
                    REGEXP ? LIMIT ?, ?"""

        page, per_page, offset = get_page_args(
        page_parameter="page",  per_page_parameter="per_page")

        paginated_journeys, journey_count = get_result_set_and_count(query=query, offset=offset, per_page=per_page, phrase=q)
        pagination = Pagination(page=page, per_page=per_page,
                            total=journey_count, css_framework="bootstrap5")

        return render_template("journeys.html", journeylist=paginated_journeys, page=page, per_page=per_page, pagination=pagination)
