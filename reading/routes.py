from fastapi import APIRouter
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

