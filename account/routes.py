from fastapi import APIRouter, Query
from http import HTTPStatus
from .account import Accounts

account_routes = APIRouter()

@account_routes.get("/all")
async def get_account_list_all(
        search_term: str | None = Query(None, description="Search term for account name or number."),
        include: str | None = Query(None, description="Include active/inactive accounts.  Valid values are 'all', 'active', 'inactive'.")
):
    '''Return a list of all accounts.'''
    accts = Accounts()
    data = accts.account_list_all(search_term=search_term, include=include)

    return {"message": "Success.", "data": data}

# account_one_details
@account_routes.get("/one/{account}")
async def get_account_one_details(account: int):
    '''Return details for one account.'''
    accts = Accounts()
    data = accts.account_one_details(account)

    return {"message": "Success.", "data": data}


@account_routes.get("/wells/{account}")
async def get_account_wells(account: int):
    '''Return a list of wells owned or partially owned for one account.'''
    accts = Accounts()
    data = accts.account_wells(account)

    return {"message": "Success.", "data": data}
