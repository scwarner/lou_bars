import csv
import requests
import sqlite3

db = sqlite3.connect('mydb.sqlite')
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS License_Data;")
cursor.execute('''CREATE TABLE License_Data (
    DataID varchar(10),
    LicenseID varchar(10),
    Description varchar(100),
    License_Name varchar(100),
    Location varchar(100),
    Street_number varchar(100),
    Prefix varchar(10),
    Street_name varchar(100),
    Suffix varchar(10),
    Longitude varchar(100),
    Latitude varchar(100),
    Expiration varchar(100),
    SubType varchar(10),
    SubDescription varchar(30),
    IssueDate varchar(10),
    ZIP_Code varchar(10),
    District varchar(5),
    Neighborhood varchar(50),
    Zoning varchar(10),
    EndorsementType varchar(30),
    EndorsementTypeDescription varchar(30),
    EndorsementStatusDescription varchar(10),
    EndorsementIssuedDate varchar(30),
    AGENCY varchar(100),
    GPSX varchar(100),
    GPSY varchar(100)
    ); 
    ''' )

CSV_URL = "https://data.louisvilleky.gov/sites/default/files/LocationBasedLicenseData_3.csv"
response = requests.get(CSV_URL)
if response.status_code != 200:
    print("Failed to get data:", response.status_code)
else:
    wrapper = csv.reader(response.text.strip().split('\n'))
    headerline = True
    for record in wrapper:
        if headerline:
            headerline = False
        else:
            cursor.execute('''INSERT INTO License_Data(DataID, LicenseID, Description, License_Name, Location, Street_number, Prefix, Street_name, Suffix, Longitude, Latitude, Expiration, SubType, SubDescription, IssueDate, ZIP_Code, District, Neighborhood, Zoning, EndorsementType, EndorsementTypeDescription, EndorsementStatusDescription, EndorsementIssuedDate, AGENCY, GPSX, GPSY)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (record))
            db.commit()
            
print(cursor.execute('SELECT * FROM License_Data;').fetchmany(3))
