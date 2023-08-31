from fastapi import APIRouter, Query

from .account import Accounts

account_routes = APIRouter()


@account_routes.get("/all")
async def get_account_list_all(
        search_term: str | None = Query(None, description="Search term for account name or number."),
        include: str |
                 None = Query(None,
                        description="Include active/inactive accounts.  Valid values are 'all', 'active', 'inactive'."),
        accounts_with_well: str |
                            None = Query(None, description="Include only accounts with wells. Valid values are '1', '0'."),

):
    """Return a list of all accounts."""
    accounts = Accounts()
    data = accounts.account_list_all(search_term=search_term, include=include, accounts_with_well=accounts_with_well)

    return {"message": "Success.", "data": data}


# account_one_details
@account_routes.get("/one/{account}")
async def get_account_one_details(account: int):
    """Return details for one account."""
    accounts = Accounts()
    data = accounts.account_one_details(account)

    return {"message": "Success.", "data": data}


@account_routes.get("/wells/{account}")
async def get_account_wells(account: int):
    """Return a list of wells owned or partially owned for one account."""
    accounts = Accounts()
    data = accounts.account_wells(account)

    return {"message": "Success.", "data": data}


@account_routes.get("/balance/{account}")
async def get_wcat_balances(account: int):
    """Return a list of water categories, category text, qty and priorities for one account."""
    accounts = Accounts()
    data = accounts.account_categories(account=account)
    return {"message": "Success.", "data": data}

@account_routes.get("/transactions/{account}")
async def get_wcat_transactions(account: int):
    """Return a list of water transactions for one account."""
    accounts = Accounts()
    data = accounts.account_transactions(account=account)
    return {"message": "Success.", "data": data}


@account_routes.get("/well-graph-data")
async def get_well_graph_data(account: int, show_wells: str = None, months: int = None):
    """Return a list of well readings for one account.  Account is required.  Show_wells and months are optional.\n
    If show_wells is not provided, return dataset contains well_id, month and acft.\n
    If months is not provided, 12 months are returned."""

    accounts = Accounts()
    data = accounts.account_well_graph_data(account=account, show_wells=show_wells, months=months)
    return {"message": "Success.", "data": data}
