from fastapi import APIRouter
from .datacalc import DataCalc

gwcalc_routes = APIRouter()


@gwcalc_routes.get("/calc/{from_date}/{to_date}/{calc_date}/{tc_code}/{code_code}/{post}")
async def get_gwcalc(from_date:str, to_date: str, calc_date: str, tc_code: str, code_code: str, post: str):
    """Perform stored procedure exec of sp_gwcalc (params) ."""

    dc = DataCalc()
    data = dc.sp_gwcalc(from_date, to_date, calc_date, tc_code, code_code, post)

    return {"message": "Success.", "data": data}


@gwcalc_routes.get("/calc_results")
async def get_gwcalc_load():
    """Retrieve data from table gwcalc_results."""
    dc = DataCalc()
    data = dc.load_results()

    return {"message": "Success.", "data": data}

@gwcalc_routes.get("/calc_status")
async def get_gwcalc_status():
    """Retrieve data from table gwcalc_status."""
    dc = DataCalc()
    data = dc.load_status()

    return {"message": "Success.", "data": data}