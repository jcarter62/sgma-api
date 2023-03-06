from http import HTTPStatus

from fastapi import APIRouter

from .wellassoc import WellAssoc

wellassoc_routes = APIRouter()


@wellassoc_routes.get("/list")
async def get_well_assoc_list():
    """Return a list of Well Associations from table sgma_wellassoc."""
    code = HTTPStatus.OK
    t = WellAssoc()
    data = t.well_assoc_all()
    if data is None:
        msg = "No records found."
        code = HTTPStatus.NO_CONTENT
    else:
        msg = "Success."
    return {"message": msg, "data": data}, code


@wellassoc_routes.get("/list/{well_id}")
async def get_well_assoc_list_one(well_id: str):
    """Return a list of Well Associations for one Well_ID from table sgma_wellassoc."""
    t = WellAssoc()
    data = t.well_assoc_one(well_id)
    if data is None:
        msg = "No records found."
    else:
        msg = "Success."
    return {"message": msg, "data": data}


@wellassoc_routes.post("/add")
async def add_well_assoc(well_id: str, account: str, amount: float, method: str, begindate: str, enddate: str,
                         ordering: int, isactive: int):
    """Add a new Well Association to table sgma_wellassoc."""
    t = WellAssoc()
    data = t.well_assoc_add(well_id, account, amount, method, begindate, enddate, ordering, isactive)
    if data is None:
        msg = "Add Record Failed."
    else:
        msg = "Success."
    return {"message": msg, "data": data}


@wellassoc_routes.get("/list_all")
async def get_well_list_all():
    """Return a list of SGMA Wells based on wmis and well associations."""
    t = WellAssoc()
    data = t.well_list_all()
    if data is None:
        msg = "No records found."
    else:
        msg = "Success."
    return {"message": msg, "data": data}


@wellassoc_routes.get("/one-well/{well_id}")
async def get_well_list_one(well_id: str):
    """Return a list of SGMA Wells based on wmis and well associations for one well_id."""
    t = WellAssoc()
    data = t.well_list_one(well_id)
    if data is None:
        msg = "No records found."
    else:
        msg = "Success."
    return {"message": msg, "data": data}


@wellassoc_routes.post("/save-well-details")
async def save_well_details(rec_id: str, well_id: str, account: str, amount: float, method: str, begindate: str,
                            enddate: str, ordering: int, isactive: int):
    """Save Well Details to table sgma_wellassoc.  If record exists, perform update, otherwise insert new record."""
    t = WellAssoc()
    # determine if record exists
    #
    # load query parameters

    data = t.lookup_one_record(rec_id)
    if data is None:
        # add new record
        data = t.insert_one_record(rec_id, well_id, account, amount, method, begindate, enddate, ordering, isactive)
        if data is None:
            msg = "Add Record Failed."
        else:
            msg = "Success."
    else:
        # update existing record
        data = t.update_one_record(rec_id, well_id, account, amount, method, begindate, enddate, ordering, isactive)
        if data is None:
            msg = "Update Record Failed."
        else:
            msg = "Success."
    return {"message": msg, "data": data}


@wellassoc_routes.post("/delete-one-record")
async def delete_one_record(rec_id: str):
    """Remove one record from table sgma_wellassoc, based on rec_id."""
    code = HTTPStatus.OK
    t = WellAssoc()
    # determine if record exists

    data = t.lookup_one_record(rec_id)
    if data is None:
        msg = "Record not found."
        code = HTTPStatus.NO_CONTENT
    else:
        # delete record
        # update existing record
        if t.delete_one_record(rec_id):
            msg = "Success."
            code = HTTPStatus.OK
        else:
            msg = "Delete Record Failed."
            code = HTTPStatus.INTERNAL_SERVER_ERROR
    return {"message": msg}, code


@wellassoc_routes.get("/account-name/{account}")
async def get_account_name(account: str):
    """Return account name."""
    code = HTTPStatus.OK
    t = WellAssoc()
    data = t.get_account_name(account)
    if data is None:
        msg = "No records found."
        code = HTTPStatus.NO_CONTENT
    else:
        msg = "Success."
    return {"message": msg, "data": data}, code


@wellassoc_routes.get("/account-details/{account}")
async def get_account_details(account: str):
    """Return account name, address, city as a string."""
    code = HTTPStatus.OK
    t = WellAssoc()
    data = t.get_account_details(account)
    if data is None:
        msg = "No records found."
        code = HTTPStatus.NO_CONTENT
    else:
        msg = "Success."
    return {"message": msg, "data": data}, code


@wellassoc_routes.get("/reorder-well-records/{well_id}")
async def reorder_well_records(well_id: str):
    """Reorder well association records for a well_id, changing the ordering field to start at 10, with step of 2."""
    code = HTTPStatus.OK
    t = WellAssoc()
    data = t.reorder_well_records(well_id)
    if data is None:
        msg = "No records found."
        code = HTTPStatus.NO_CONTENT
    else:
        msg = "Success."
    return {"message": msg, "data": data}, code


@wellassoc_routes.get("/well-details/{well_id}")
async def get_well_details(well_id: str):
    """Lookup a well in wmis, and return details of this well.  Including
    well_id, Description, SerialNo, number of associated sgma_wellassoc records,
    and the sum of the amount field for each associated sgma_wellassoc record. """
    code = HTTPStatus.OK
    t = WellAssoc()
    data = t.get_well_details(well_id)
    if data is None:
        msg = "No records found."
        code = HTTPStatus.NO_CONTENT
    else:
        msg = "Success."
    return {"message": msg, "data": data}, code
