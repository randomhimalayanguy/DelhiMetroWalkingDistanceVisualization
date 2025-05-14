# Delhi Metro Station Coordinates and Map

This Python project scrapes data from Wikipedia to collect the names and coordinates (latitude and longitude) of all Delhi Metro stations. 
It then generates a CSV file and visualizes each station on an interactive Folium map with a 1km circle radius to represent the walking distance.

---

## Features

- Scrapes all Delhi Metro station names from Wikipedia (https://en.wikipedia.org/wiki/List_of_Delhi_Metro_stations)
- Fetches coordinates from individual Wikipedia page of metro stations.
- Converts DMS (Degrees, Minutes, Seconds) format to Decimal Degrees (for coordinates)
- Generates a CSV file (`Metro_stations.csv`) if it doesn't already exist
- Uses Folium to generate an interactive map with markers and radius circles
- Highlights stations with missing coordinates

---

## Requirements

- `requests`
- `beautifulsoup4`
- `pandas`
- `folium`

You can install them using:

```bash
pip install -r requirements.txt

