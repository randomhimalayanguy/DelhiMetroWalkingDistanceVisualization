from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import folium
import os


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


def generate_metro_station_csv(output_name):
    # URL from which data is fetched
    URL = "https://en.wikipedia.org/wiki/List_of_Delhi_Metro_stations"
    page = requests.get(URL)

    # Parsing the main page
    soup = BeautifulSoup(page.text, "html.parser")
    # There are 3 tables with class as wikitable
    tables = soup.find_all("table", attrs={"class":["wikitable"]})
    table = tables[2] # Our requried table 3rd table

    stations = [] # To store names of stations
    latitude = []    # To store latitude of stations
    longitude = []   # To store longitude of stations

    # Set to store colors of metro lines, useful since table is not perfectly formatted
    colors = {"Pink", "Violet", "Yellow", "Blue", "Red", 
            "Green", "Magenta", "Airport", "Grey"}


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

                        cur_latitude = new_soup.find("span", attrs={"class":["latitude"]})
                        cur_longitude = new_soup.find("span", attrs={"class":["longitude"]})
                        
                        # Add coordinates if exist, else add None
                        latitude.append(dms_to_dd(cur_latitude.text) if cur_latitude else None)
                        longitude.append(dms_to_dd(cur_longitude.text) if cur_longitude else None)


        # Creating dataframe
        df = pd.DataFrame({"Station Name" : stations, "latitude":latitude, "longitude":longitude})
        print(df.head())    # Printing the head of dataframe
        df.to_csv(output_name) # Exporting the .csv file

    # If correct table is not found
    else:
        print("Table not found")


CSV_FILE_PATH = "Metro_stations.csv"
map_file_name = "delhi_metro_1km_circles"


if not os.path.exists(CSV_FILE_PATH):
    print("File does not exist, Generating file")
    generate_metro_station_csv(CSV_FILE_PATH)


try:
    stations = pd.read_csv(CSV_FILE_PATH)  # Contains 'Station', 'Latitude', 'Longitude'
    stations_without_coord = stations[stations["latitude"].isnull()]
    print(f"Stations which do not have coordinates. Total = {len(stations_without_coord)}\n", stations_without_coord["Station Name"])
    stations = stations.dropna()

    # Create a base map centered on Delhi
    m = folium.Map(location=[28.6139, 77.2090], zoom_start=11)
    
    # Add circles for each station
    for index, row in stations.iterrows():
        folium.Circle(
            location=[row['latitude'], row['longitude']],
            radius=1000,  #  1km
            color='blue',
            fill=True,
            fill_opacity=0.2,
            popup=row['Station Name']
        ).add_to(m)

        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(row['Station Name'], parse_html=True),
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
    
    # Save the map to an HTML file
    m.save(f'{map_file_name}.html')
    print("Total stations ", len(stations))

except Exception as e:
    print(f"There is a problem, {e}")
