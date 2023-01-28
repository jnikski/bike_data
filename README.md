# HELSINKI CITY BIKE APP

- Application for viewing bike data. Python, Flask, MariaDB.

## Installation

- Prerequisites: Python 3.10.6, pip, Windows Subsystem for Linux or Ubuntu

## Virtual environment

- Install necessary modules `sudo apt install python3-dev python3-venv`
- Create virtualenv in project root directory `python3 -m venv env`
- Activate virtual environment `source env/bin/activate`
- Install dependencies `pip install -r requirements.txt`

### Database and validation

- Install mariadb database `sudo apt install mariadb-server`. In WSL mariadb service is started this way `sudo service mariadb start`
- Run `./validate.sh` to download csv files and to validate data. Optionally download project relevant csv files to the data directory and in /data, run `python validate_data.py` within the activated virtualenv.
- Set absolute filepaths for the two `LOAD DATA LOCAL INFILE` commands in the `data/bike.sql`
- import data to mariadb `sudo mariadb < /<path>/<to>/bike_db.sql`

### Flask app

Run app: `flask run`. With debugging enabled: `flask --debug run`.

#### Creating stations/journeys

`/station/create` and `/journey/create` endpoints take JSON object that must be sent with POST request. Objects must contain the following fields:

##### Station

1. `nimi`, `namn`, `name`, `osoite`, `adress`, `stad`, `operaattor`: String
2. `kapasiteet`, `x`, `y`: Number

##### Journey

1. `departure_time`, `return_time`: Datetime
2. `departure_station_id`, `return_station_id`: Integer
3. `departure_station`, `return_station`: String
4. `covered_distance`, `duration`: Number
