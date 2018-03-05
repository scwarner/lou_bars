import csv
import requests
import sqlite3

db = sqlite3.connect('mydb.sqlite')
cur = db.cursor()
cur.execute('''CREATE TABLE License_Data (
    ID varchar(10),
    LicenseID varchar(10),
    Description; ''' )

CSV_URL = "https://data.louisvilleky.gov/sites/default/files/LocationBasedLicenseData_1.csv"
response = requests.get(CSV_URL)
if response.status_code != 200:
    print("Failed to get data:", response.status_code)
else:
    wrapper = csv.reader(response.text.strip().split('\n'))
    for record in wrapper:
        print(record)
