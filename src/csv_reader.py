import csv


def get_trucks():
    data = []
    with open('data/trucks.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['lat'] = float(row['lat'])
            row['lng'] = float(row['lng'])
            data.append(row)
    return data


def get_cargos():
    data = []
    with open('data/cargo.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['origin_lat'] = float(row['origin_lat'])
            row['origin_lng'] = float(row['origin_lng'])
            data.append(row)
    return data
