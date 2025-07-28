import json
import csv

with open('all_cars.json') as f:
    data = json.load(f)

with open('hotwheels.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['toy_num', 'col_num', 'model', 'series', 'series_num', 'photo_url', 'year'])

    for car in data:
        try:
            writer.writerow([
                car.get('toy_num', [''])[0],
                car.get('col_num', [''])[0],
                ' '.join(car.get('model', [])),
                car.get('series', [''])[0],
                car.get('series_num', [''])[0],
                car.get('photo_url', [''])[0],
                int(car.get('year', 0))
            ])
        except Exception as e:
            print(f"Error parsing row: {car} -> {e}")
