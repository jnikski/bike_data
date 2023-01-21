DROP DATABASE IF EXISTS bike;
CREATE DATABASE bike;
USE bike;

CREATE TABLE station (
fid INT,
id INT NOT NULL AUTO_INCREMENT,
nimi VARCHAR(50) NOT NULL,
namn VARCHAR(50),
name VARCHAR(50) NOT NULL,
osoite VARCHAR(60) NOT NULL,
adress VARCHAR(60) NOT NULL,
kaupunki VARCHAR(20) NOT NULL,
stad VARCHAR(20) NOT NULL,
operaattor VARCHAR(50) NOT NULL,
kapasiteet INT NOT NULL,
x FLOAT NOT NULL,
y FLOAT NOT NULL,
PRIMARY KEY (id)
);

CREATE TABLE journey (
departure_time DATETIME NOT NULL, 
return_time DATETIME NOT NULL,
departure_station_id INT NOT NULL,
departure_station VARCHAR(50),
return_station_id INT NOT NULL,
return_station VARCHAR(50) NOT NULL,
covered_distance FLOAT NOT NULL,
duration DECIMAL NOT NULL,
FOREIGN KEY (departure_station_id) REFERENCES station(id),
FOREIGN KEY (return_station_id) REFERENCES station(id)
);
-- Insert valid absolute path /<path>/<to>/bike_data/data/Helsingin_ja_Espoon_kaupunkipyöräasemat_avoin.csv' 
LOAD DATA LOCAL INFILE '/<path>/<to>bike_data/data/Helsingin_ja_Espoon_kaupunkipyöräasemat_avoin.csv' 
    INTO TABLE station 
    FIELDS 
        TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS (FID,ID,Nimi,Namn,Name,Osoite,Adress,Kaupunki,Stad,Operaattor,Kapasiteet,x,y);

-- Insert valid absolute path: /<path>/<to>/bike_data/data/validated_bike_data.csv
LOAD DATA LOCAL INFILE '/<path>/<to>/bike_data/data/validated_bike_data.csv' 
    INTO TABLE journey 
    FIELDS 
        TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\r\n';