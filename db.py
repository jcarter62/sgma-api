from fastapi import APIRouter
from wmisdb import Turnouts


db_route = APIRouter()


@db_route.get("turnout")
async def get_turnouts():
    t = Turnouts()
    data = t.data()
    records = data.__len__()
    if records == 0:
        msg = "No records found."
    else:
        msg = "Success."
    return {"message": msg, "records": records, "data": data}


@db_route.get("turnout/{turnout_id}")
async def get_turnout(turnout_id: str):
    t = Turnouts(turnout_id)
    data = t.data()
    records = data.__len__()
    if records == 0:
        msg = "No records found."
    else:
        msg = "Success."
    return {"message": msg, "records": records, "data": data}


