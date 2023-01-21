# BIKE WEB APP

## Installation
* Prerequisites: Python 3.10.6, pip, Windows Subsystem for Linux or Ubuntu
## Virtual environment
* Run virtualenv in project root directory `python3 -m venv env`
* Activate virtual environment `source env/bin/activate`
* Install dependencies `pip install -r requirements.txt`
### Database and validation
* First install mariadb database `sudo apt install mariadb-server`. In WSL mariadb service is started this way `sudo service mariadb start`
* Download `Helsingin_ja_Espoon_kaupunkipyöräasemat_avoin.csv`, `2021-05.csv, 2021-06.csv`, `2021-07.csv` to the 'data' directory
* Run `./validate.sh` to validate data
* Before importing data, a *valid absolute path* should be set for the two `LOAD DATA LOCAL INFILE` queries in the `data/bike.sql`
* import data to mariadb `sudo mariadb < /<path>/<to>/bike_db.sql`
### Flask app 
Set environment variable for Flask in the shell: `export FLASK_APP=run.py`. Optionally `export FLASK_DEBUG=1` to run app in development mode.
Run flask: `flask run`. The project is served at `http://localhost:5000`