from typing import Union
from fastapi import FastAPI
import folium
import requests

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}






@app.get("/location/{place_name}/")
def get_coordinate(place_name, prefecture= ""):

def main():
    lat = 34.959377,
    lon = 132.1442749
    location = get_location(lat, lon)
    print(location)

    place_name  = "島根県立しまね海洋館(アクアス)"
    place = get_coordinate(place_name, prefecture= "")
    print(place)



if __name__ == "__main__":
    main()
