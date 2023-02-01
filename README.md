# HELSINKI CITY BIKE APP

---

- Application for viewing bike data. Python, Flask, MariaDB.

## Prerequisites

- Python 3.10, Windows Subsystem for Linux and/or Ubuntu 22.04.

## Virtual environment

- Install necessary packages `sudo apt install python3-dev python3-venv libmariadb-dev -y`
- Create virtualenv in project root directory `python3 -m venv env`
- Activate virtual environment `source env/bin/activate`
- Install dependencies within the virtual environment `pip install -r requirements.txt`

### Data validation

- Download and validate data by running `./validate.sh`. Optionally move project relevant csv files to the data directory and in /data, run `python validate_data.py` within the virtual environment.
As a result, `/data/validated_bike_data.csv` is created.

### Dockerizing

[Docker](https://docs.docker.com/engine/install/ubuntu/) and [Docker-compose](https://docs.docker.com/compose/install/linux/) must be installed and data validation done.

Depending on the Docker Compose version, command `docker-compose up -d` or `docker compose up -d` will launch containerized project. Note: It takes about 25 seconds for the app to get database connection after the command has finished.

### Installing without containers

- Activate virtual environment `source env/bin/activate`.
- Validate data if not done yet.
- Install mariadb database `sudo apt install mariadb-server`. In WSL mariadb service is started this way `sudo service mariadb start`.
- Set valid absolute csv filepaths for the two `LOAD DATA LOCAL INFILE` commands in the `data/bike.sql`.
- import data to mariadb `sudo mariadb < /<path>/<to>/bike_db.sql`.
- Run app: `flask run`. With debugging enabled: `flask --debug run`.

## Creating stations/journeys

`/station/create` and `/journey/create` endpoints take JSON object that must be sent with POST request. Objects must contain the following fields:

### Station

1. `nimi`, `namn`, `name`, `osoite`, `adress`, `stad`, `operaattor`: String.
2. `kapasiteet`, `x`, `y`: Number.

### Journey

1. `departure_time`, `return_time`: Datetime.
2. `departure_station_id`, `return_station_id`: Integer.
3. `departure_station`, `return_station`: String.
4. `covered_distance`, `duration`: Number.
