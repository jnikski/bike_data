# HELSINKI CITY BIKE APP

---

- Application for viewing bike data. Python, Flask, MariaDB.

## Installation

- Prerequisites: Python 3.10, Windows Subsystem for Linux and/or Ubuntu 22.04.

### Virtual environment

- Install necessary modules `sudo apt install python3-dev python3-venv`
- Create virtualenv in project root directory `python3 -m venv env`
- Activate virtual environment `source env/bin/activate`
- Install dependencies within virtual environment `pip install -r requirements.txt`

### Dockerizing

[Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04) and [Docker-compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04) must be installed.

Easiest way to start containers is `./dockerize.sh`. This will also download and validate the csv data.

If validation is already done via `./validate.sh`, command `docker-compose up -d` will be enough. It takes a few seconds for the app to get database connection after the command has finished.

### Installing without containers

- Install mariadb database `sudo apt install mariadb-server`. In WSL mariadb service is started this way `sudo service mariadb start`.
- Activate virtual environment `source env/bin/activate`.
- Run `./validate.sh` to download csv files and to validate data. Optionally download project relevant csv files to the data directory and in /data, run `python validate_data.py`.
- Set valid absolute csv filepaths for the two `LOAD DATA LOCAL INFILE` commands in the `data/bike.sql`.
- import data to mariadb `sudo mariadb < /<path>/<to>/bike_db.sql`
- Run app: `flask run`. With debugging enabled: `flask --debug run`.

## Creating stations/journeys

`/station/create` and `/journey/create` endpoints take JSON object that must be sent with POST request. Objects must contain the following fields:

### Station

1. `nimi`, `namn`, `name`, `osoite`, `adress`, `stad`, `operaattor`: String
2. `kapasiteet`, `x`, `y`: Number

### Journey

1. `departure_time`, `return_time`: Datetime
2. `departure_station_id`, `return_station_id`: Integer
3. `departure_station`, `return_station`: String
4. `covered_distance`, `duration`: Number
