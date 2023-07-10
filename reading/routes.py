"""
Routes for reading module.
"""
import base64

from fastapi import APIRouter
import datetime
import json
from .reading import Reading

reading_routes = APIRouter()


@reading_routes.get("/last/{well_id}")
async def get_last_reading(well_id: str):
    """Return most recent well reading."""
    t = Reading()
    data = t.last_reading(well_id)
    if data is None:
        msg = "No records found."
    else:
        msg = "Success."
    return {"message": msg, "data": data}


# last_year
@reading_routes.get("/lastyear/{well_id}")
async def get_last_year(well_id: str):
    """Return last year's well readings."""
    t = Reading()
    data = t.last_year(well_id)
    if data is None:
        msg = "No records found."
    else:
        msg = "Success."
    return {"message": msg, "data": data}


# list of meters that are active
@reading_routes.get("/meters")
async def get_meters():
    """Return list of meters."""
    t = Reading()
    data = t.meters()
    if data is None:
        msg = "No records found."
    else:
        msg = "Success."
    return {"message": msg, "data": data}


@reading_routes.post("/add")
async def add_reading(params):
# async def add_reading(well_id: str, reading: float, operator: str,
#                       read_date: str = None, read_time: str = None,
#                       note: str = None, ):
    """Add a new reading to table"""
    import uuid

    reading_guid = uuid.uuid4().__str__()
    reading_guid = reading_guid.lower()
    reading_guid = reading_guid.replace('-', '')

    # decode params from base64 encoded string
    params = params.encode('ascii')
    params = base64.b64decode(params)

    # convert params in JSON.stringify to dict
    params = json.loads(params)

    params['note'] = ''

    if params['readingdate'] is None:
        params['readingdate'] = datetime.datetime.now().strftime("%Y-%m-%d")

    if params['readingtime'] is None:
        params['readingtime'] = datetime.datetime.now().strftime("%H:%M:%S")


    t = Reading()
    data = t.add_reading(well_id=params['meter_id'],
                         date=params['readingdate'],
                         time=params['readingtime'],
                         reading=params['readingvalue'],
                         operator=params['user_name'],
                         note=params['note'],
                         guid=reading_guid)

    if data is None:
        msg = "Add Record Failed."
    else:
        msg = "Success."

    return {"message": msg, "data": data}


@reading_routes.post("/process_pendings")
async def process_pending_readings():
    """Process pending readings."""
    t = Reading()
    data = t.process_pending_readings()

    if data is None:
        msg = "Process Pending Reading Failed."
    else:
        msg = "Success."

    return {"message": msg, "data": data}


@reading_routes.get("/well-status")
async def get_well_status():
    """Return list of wells and their status."""
    t = Reading()
    data = t.get_well_status()
    if data is None:
        msg = "No records found."
    else:
        msg = "Success."
    return {"message": msg, "data": data}

