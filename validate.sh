#!/bin/bash
source env/bin/activate
cd data
python validate_data.py 2021-05.csv 2021-06.csv 2021-07.csv
deactivate

