from fastapi import APIRouter
from decouple import config

misc_routes = APIRouter()


@misc_routes.get("/dbinfo")
async def get_misc_dbinfo():
    """Return database info as object."""
    dbname = config('DATABASE', default='unknown')

    data = dbname

    return {"message": "Success.", "data": data}

