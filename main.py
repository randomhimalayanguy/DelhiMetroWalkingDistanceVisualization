from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# URL from which data is fetched
URL = "https://en.wikipedia.org/wiki/List_of_Delhi_Metro_stations"
page = requests.get(URL)

# Parsing the main page
soup = BeautifulSoup(page.text, "html.parser")
# There are 3 tables with class as wikitable
tables = soup.find_all("table", attrs={"class":["wikitable"]})
table = tables[2] # Our requried table 3rd table

stations = [] # To store names of stations
lat = []    # To store latitude of stations
long = []   # To store longitude of stations

# Set to store colors of metro lines, useful since table is not perfectly formatted
colors = {"Pink", "Violet", "Yellow", "Blue", "Red", 
          "Green", "Magenta", "Airport", "Grey"}

# We are getting coordinates data in the form of degree, min and sec, converting it to decimals
def dms_to_dd(dms_str):
    # Example: '28°42′59.526″N' -> 28.716535
    if not dms_str:
        return None
    
    # Strip the string -> °, ′, ″, N S E W
    match = re.match(r"(\d+)°(\d+)′([\d.]+)″([NSEW])", dms_str.strip())
    if not match:
        return None

    degrees, minutes, seconds, direction = match.groups()
    dd = float(degrees) + float(minutes)/60 + float(seconds)/3600

    if direction in ['S', 'W']:
        dd *= -1

    return round(dd, 6)


# if our table exist
if table:
    rows = table.find_all("tr")[1:] # All rows of table, except the heading
    # Iterating over all rows
    for row in rows:
        col = row.find_all("td")    # Each row has multiple columns
        if col:
            # Storing the content of <a> tag of first column, since it contains all useful info
            link = col[0].find("a") 
            # if link exist and has 'title' -> name of metro station
            if link and link.has_attr("title"):
                station_name = link["title"]
                # Due to formatting of table, interchange stations are giving Metro line color name, skipping them
                if station_name.split(" ")[0] not in colors:
                    stations.append(station_name) # Since correct station name, adding it to list
                    
                    # Fetching the station coordinates from each station's wiki page
                    cur_station_page_link = "https://en.wikipedia.org" + link["href"]
                    page = requests.get(cur_station_page_link)
                    new_soup = BeautifulSoup(page.text, "html.parser")

                    latitude = new_soup.find("span", attrs={"class":["latitude"]})
                    longitude = new_soup.find("span", attrs={"class":["longitude"]})
                    if latitude:
                        lat.append(dms_to_dd(latitude.text))
                        long.append(dms_to_dd(longitude.text))
                    else:
                        lat.append(None)
                        long.append(None)

    # Creating dataframe
    df = pd.DataFrame({"Station Name" : stations, "latitude":lat, "longitude":long})
    print(df.head())    # Printing the head of dataframe
    df.to_csv("Metro_stations.csv") # Exporting the .csv file

# If correct table is not found
else:
    print("Not found")



