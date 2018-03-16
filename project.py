import csv
import requests
import sqlite3
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource

#ABC_data = requests.get('https://data.louisvilleky.gov/sites/default/files/LocationBasedLicenseData_3.csv')
#raw_text = ABC_data.text

#license_list = raw_text.split('\r')
#formatted_list = [r.split(',') for r in license_list] 
#[del r[5:9] for r in formatted_list]
#for row in formatted_list:
 #   del row[5:9]
#print(formatted_list[3])

db = sqlite3.connect('mydb.sqlite')
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS License_Data;")
cursor.execute('''CREATE TABLE License_Data (
    DataID varchar(10),
    LicenseID varchar(10),
    Description varchar(100),
    License_Name varchar(100),
    Location varchar(100),
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
        del record[5:9]
        if headerline:
            headerline = False
        else:
            cursor.execute('''INSERT INTO License_Data(DataID, LicenseID, Description, License_Name, Location, Longitude, Latitude, Expiration, SubType, SubDescription, IssueDate, ZIP_Code, District, Neighborhood, Zoning, EndorsementType, EndorsementTypeDescription, EndorsementStatusDescription, EndorsementIssuedDate, AGENCY, GPSX, GPSY)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (record))
            db.commit()

bar_per_zip = cursor.execute("""SELECT COUNT(DISTINCT License_Name), ZIP_Code FROM License_Data 
                                    WHERE SubDescription = 'Bar' OR EndorsementTypeDescription = 'Microbrewery' 
                                    GROUP BY ZIP_Code;""")
nums_zips = bar_per_zip.fetchall()

bar_nums = [row[0] for row in nums_zips]
zip_codes = [row[1] for row in nums_zips]

#print(bar_nums)
#print(zip_codes)
output_file("lou_barchart.html")

source = ColumnDataSource(data=dict(zip_codes=zip_codes, bar_nums=bar_nums))

p = figure(x_range=zip_codes, y_range=bar_nums, plot_height=600, toolbar_location=None, title="Bars Per ZIP Code")
p.vbar(x="zip_codes", top="bar_nums", width=0.9, color="#2868C7")

p.xgrid.grid_line_color = None
p.y_range.start = 0
p.y_range.end = 40
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)
