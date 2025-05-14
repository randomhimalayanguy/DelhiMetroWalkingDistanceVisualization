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
## Metro stations CSV file - 

|   | Station Name               | latitude  | longitude |
| - | -------------------------- | --------- | --------- |
| 0 | Adarsh Nagar metro station | 28.736534 | 77.163409 |
| 1 | AIIMS metro station        | 28.567083 | 77.210226 |
| 2 | Akshardham metro station   | 28.613338 | 77.277326 |
| 3 | Anand Vihar metro station  | 28.647884 | 77.315540 |
| 4 | Arjan Garh metro station   | 28.480299 | 77.125617 |

---

## Map output

![image](https://github.com/user-attachments/assets/61502f87-6427-45d8-ad76-6e91cf1c1ecc)


---

## Requirements

- `requests`
- `beautifulsoup4`
- `pandas`
- `folium`

You can install them using:

```bash
pip install -r requirements.txt

