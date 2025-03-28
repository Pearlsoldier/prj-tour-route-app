from typing import Union
from fastapi import FastAPI
from location.management import LocationManager, MappingManager

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/location/{place_name}/")
def get_coordinates(place_name):
    try:
        locator = LocationManager(place_name)
        return locator.locations_data
    except Exception as e:
        return e

@app.get("/map/{location}/")
def mapping(location):
    try:
        map = MappingManager(location)
        return map.initmap
    except Exception as e:
        return e

def main():
    pass


if __name__ == "__main__":
    main()
