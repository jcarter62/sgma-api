"""
The main module of the sgma-api system
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from decouple import config, UndefinedValueError
from parcel import parcel_routes
from wellassoc import wellassoc_routes
from account import account_routes
from reading import reading_routes


app = FastAPI()

app.include_router(parcel_routes, prefix="/parcel", tags=["parcel"])
app.include_router(wellassoc_routes, prefix="/well-assoc", tags=["well-assoc"])
app.include_router(account_routes, prefix="/account", tags=["account"])
app.include_router(reading_routes, prefix="/reading", tags=["reading"])


def is_allowed(host_ip) -> bool:
    """
    Check if the host ip is allowed to access the resource based on ALLOWD_IPS environment variable

    :param host_ip: The host ip address
    :return: True if the host ip is allowed, False otherwise
    """
    try:
        ip_addresses = config('ALLOWED_IPS', default='')

        if ip_addresses == '':
            return True

        allowd_ips = ip_addresses.split(',')
        return host_ip in allowd_ips
    except UndefinedValueError as err:
        print(f'Error which checking allowd IPs: {err}')
        return False


@app.get("/")
async def root():
    """
    The root path of the API
    """
    return {"message": "Welcome to the sgma-api System."}


@app.middleware("http")
async def before_request(request: Request, call_next):
    """
    Middleware to check if the host ip is allowed to access the resource
    """
    try:
        method = request.method
        path = request.url.path
        print(f"method: {method}, path: {path}")
        ip_addr = str(request.client.host)
        if not is_allowed(ip_addr):
            data = {"message": f"IP {ip_addr} is not allowed to access this resource"}
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)
        response = await call_next(request)
    finally:
        pass
    return response
