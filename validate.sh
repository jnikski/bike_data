#!/bin/bash
cd data
echo -e "\nDownloading csv files..\n"
curl -LJ https://opendata.arcgis.com/datasets/726277c507ef4914b0aec3cbcfcbfafc_0.csv -o Helsingin_ja_Espoon_kaupunkipyöräasemat_avoin.csv
curl -LOJ https://dev.hsl.fi/citybikes/od-trips-2021/2021-0[5-7].csv

source ../env/bin/activate
python validate_data.py 2021-0[5-7].csv
deactivate