import csv
import json


with open("input.csv", "r", newline="") as csv_file:
    reader = csv.DictReader(csv_file)

    data = list(reader)

with open("output.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("CSV data successfully converted to JSON.")
print("Output stored in output.json")