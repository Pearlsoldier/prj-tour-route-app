import sys
import os
import pprint
import uuid


from geocoding.geocoding import Geocoding, ReverseGeocoding
from location.locations import Location, AccessibleLocation
from interface.input_parser import (
    InterfaceAdministrator,
    InterfaceBatch,
    CidInterfaceBatch,
)

from transport.transport import Walk
from transittime.timerequired import TimeRequired
from DB.database import DatabaseService
from sql.postgresql import QueryBuilder
from batch.preprocessing import DatabasePreprocessing


def main():

    sql_handler = QueryBuilder()
    batch_insert = sql_handler.insert_cid_datasets()


if __name__ == "__main__":
    main()
