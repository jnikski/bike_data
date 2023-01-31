#!/bin/bash
./validate.sh
docker-compose up -d
echo "App starting in a few seconds at http://localhost/"
echo "Please be patient.."