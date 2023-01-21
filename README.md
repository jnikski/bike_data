# BIKE WEB APP
- Application for viewing bike data. Python, Flask, MariaDB.
## Installation
* Prerequisites: Python 3.10.6, pip, Windows Subsystem for Linux or Ubuntu
## Virtual environment
* Create virtualenv in project root directory `python3 -m venv env`
* Activate virtual environment `source env/bin/activate`
* Install dependencies `pip install -r requirements.txt`
### Database and validation
* Install mariadb database `sudo apt install mariadb-server`. In WSL mariadb service is started this way `sudo service mariadb start`
* Run `./validate.sh` to download csv files and to validate data. Optionally download project relevant csv files to the data directory and in /data, run `python validate_data.py` within the activated virtualenv.
* Set absolute filepaths for the two `LOAD DATA LOCAL INFILE` commands in the `data/bike.sql`
* import data to mariadb `sudo mariadb < /<path>/<to>/bike_db.sql`
### Flask app 
Set environment variable for Flask in the shell: `export FLASK_APP=run.py`. Optionally `export FLASK_DEBUG=1` to run app in development mode.
Run flask: `flask run`. The project is served at `http://localhost:5000`