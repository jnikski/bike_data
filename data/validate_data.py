import sys
import datetime
import csv
import os
import pandas as pd

no_duplicates = 'no_duplicates.csv'
validated_bike_data = 'validated_bike_data.csv'

totalrows = 0
writtenrows = 0
totalfails = 0


def concatenate_files_remove_duplicates(files):
    print('Concatenating files..')

    df_csv_concat = pd.concat([pd.read_csv(file)
                               for file in files], ignore_index=True)

    df = pd.DataFrame(df_csv_concat, columns=[
        'Departure', 'Return', 'Departure station id', 'Departure station name', 'Return station id', 'Return station name', 'Covered distance (m)', 'Duration (sec.)'])

    print(f'Total rows: {len(df)}')
    print(f'Removing {len(df)-len(df.drop_duplicates())} duplicated rows..')

    df = df.drop_duplicates()

    df.to_csv(no_duplicates, index=False)


def validate_fields(row):

    # If all fields exist
    if len(row) != 8:
        return False

    # Validate dates in the first and second index.
    for j in range(2):

        try:

            bool(datetime.datetime.strptime(row[j], "%Y-%m-%dT%H:%M:%S"))

        except ValueError:
            return False

    # Check if station id's are in 'Helsingin_ja_Espoon_kaupunkipyöräasemat.csv'
    try:

        if int(row[2]) not in stationIDs:
            return False

        elif int(row[4]) not in stationIDs:
            return False

    except ValueError as e:
        return False

    # Covered distance, no distances below 10m or duration 10 sec
    try:

        if float(row[6]) < 10.0 or float(row[7]) < 10.0:
            return False

    except ValueError as e:
        return False

    else:
        return True


stationIDs = []
with open('Helsingin_ja_Espoon_kaupunkipyöräasemat_avoin.csv', 'r') as stations_csv:
    reader = csv.reader(stations_csv)
    next(reader, None)

    for row in reader:
        if int(row[1]):
            stationIDs.append(int(row[1]))
    stationIDs.sort()

try:

    if len(sys.argv) == 1:
        concatenate_files_remove_duplicates(
            ["2021-05.csv", "2021-06.csv", "2021-07.csv"])

    elif len(sys.argv) > 1:
        concatenate_files_remove_duplicates(
            [sys.argv[i] for i in range(len(sys.argv)) if i > 0])

except: 
    print('Wrong file names given or files are not in the /data directory. Exiting..')
    sys.exit()


# Write row to file if all fields are valid
with open(validated_bike_data, 'w+') as result:
    writer = csv.writer(result, delimiter=',')

    with open(no_duplicates, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)

        print('Validating csv fields..')
        for row in reader:
            totalrows += 1

            if validate_fields(row):
                writer.writerow(row)
                writtenrows += 1
            else:
                totalfails += 1


if os.path.exists(no_duplicates):
    os.remove(no_duplicates)

print(
    f'Unduplicated rows: {totalrows}. Failed rows: {totalfails}. Written rows: {writtenrows}')
print(f'Data validated. Created "/data/{validated_bike_data}".')