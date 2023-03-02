from fastapi import APIRouter
from .parcel import Parcels

parcel_routes = APIRouter()


@parcel_routes.get("/list")
async def get_parcellist():
    '''Return a list of parcels_id values.'''
    t = Parcels()
    data = t.parcel_list()
    if data is None:
        msg = "No records found."
    else:
        msg = "Success."
    return {"message": msg, "data": data}


@parcel_routes.get("/details/{parcel_id}")
async def get_parcel_details(parcel_id: str):
    '''Return parcel details for a single parcel_id.  The result includes all fields from the parcel table.'''
    t = Parcels(parcel_id=parcel_id)
    data = t.parcel_details()
    if data is None:
        msg = "No records found."
    else:
        msg = "Success."
    return {"message": msg, "data": data}


@parcel_routes.get("/sgma-acres/{parcel_id}")
@parcel_routes.get("/sgma-acres/")
async def get_parcels(parcel_id: str = None):
    '''Return parcel details for all or a single parcel_id.
    The result includes the following fields:
    parcel_id, isactive, legaldesc, acres, eligible, spa, row_number
    '''
    t = Parcels(isactive=1, parcel_id=parcel_id)
    data = t.parcel_details_w_acres()
    if data.__len__() == 0:
        msg = "No records found."
    else:
        msg = "Success."
    return {"message": msg, "data": data}

