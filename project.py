import csv
import requests
import sqlite3
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource

# Connect to SQLite database and create table
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
    ''')

# Request data from Louisville Open Data
CSV_URL = "https://data.louisvilleky.gov/sites/default/files/LocationBasedLicenseData_1.csv"
response = requests.get(CSV_URL)
if response.status_code != 200 and response.status_code != 404:
    print("Failed to get data:", response.status_code)
# If URL is not available, pull data from CSV file in Data and insert into table
elif response.status_code == 404:
    with open('data/LocationBasedLicenseData_3.csv', newline='') as csvfile:
        wrapper = csv.reader(csvfile)
        headerline = True
        for record in wrapper:
            del record[5:9]  # Remove columns with duplicate data from CSV file
            if headerline:
                headerline = False
            else:
                cursor.execute('''INSERT INTO License_Data(DataID, LicenseID, Description, License_Name, Location, Longitude, Latitude, Expiration, SubType, SubDescription, IssueDate, ZIP_Code, District, Neighborhood, Zoning, EndorsementType, EndorsementTypeDescription, EndorsementStatusDescription, EndorsementIssuedDate, AGENCY, GPSX, GPSY)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (record))
                db.commit()
# Insert text from URL response into table
else:
    wrapper = csv.reader(response.text.strip().split('\n'))
    headerline = True
    for record in wrapper:
        del record[5:9]  # Remove columns with duplicate data from CSV file
        if headerline:
            headerline = False
        else:
            cursor.execute('''INSERT INTO License_Data(DataID, LicenseID, Description, License_Name, Location, Longitude, Latitude, Expiration, SubType, SubDescription, IssueDate, ZIP_Code, District, Neighborhood, Zoning, EndorsementType, EndorsementTypeDescription, EndorsementStatusDescription, EndorsementIssuedDate, AGENCY, GPSX, GPSY)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (record))
            db.commit()

# SQL query to find out number of bars per District
bar_per_district = cursor.execute("""SELECT COUNT(DISTINCT License_Name), District
                                    FROM License_Data
                                    WHERE SubDescription = 'Bar'
                                    OR EndorsementTypeDescription = 'Microbrewery'
                                    OR License_Name LIKE '%Bar%' OR License_Name LIKE '%Pub%' OR License_Name LIKE'%Tavern%'
                                    GROUP BY District
                                    ORDER BY COUNT(DISTINCT License_Name) DESC;""")

# Save results from query into a variable
nums_districts = bar_per_district.fetchall()

# Create two lists: One for number of bars and the other for corresponding districts
bar_nums = [row[0] for row in nums_districts]
districts = [row[1] for row in nums_districts]

#print(bar_nums)
#print(districts)

# Output to HTML file
output_file("lou_barchart.html")

# Determine how data will be visualized
source = ColumnDataSource(data=dict(
    districts=districts[:10],
    bar_nums=bar_nums[:10],
    color=['#ec7628', '#2868c7', '#ec7628', '#ec7628', '#ec7628', '#ec7628', '#ec7628', '#ec7628', '#ec7628', '#ec7628'],
    label=['Other', 'Highlands District', 'Other', 'Other', 'Other', 'Other', 'Other', 'Other', 'Other', 'Other']))

# Determine which tools to include in chart
TOOLTIPS = 'pan, box_zoom, reset, save'

# Create a new plot with toolbar information and title
p = figure(x_range=districts[:10], plot_width=900, plot_height=400, toolbar_location='below', tools=TOOLTIPS, title="Where are the most watering holes in Louisville?")

# Create bar chart with data saved in source
p.vbar(x='districts', width=0.5, bottom=0, top='bar_nums', color='color', legend='label', source=source)

p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.axis_label = "Districts with highest number of bars in Louisville"
p.yaxis.axis_label = "Number of bars per district"

# Show the results
show(p)
