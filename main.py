from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from parcel import parcel_routes
from wellassoc import wellassoc_routes
from account import account_routes
from decouple import config


app = FastAPI()

app.include_router(parcel_routes, prefix="/parcel", tags=["parcel"])
app.include_router(wellassoc_routes, prefix="/well-assoc", tags=["well-assoc"])
app.include_router(account_routes, prefix="/account", tags=["account"])


def is_allowed(host_ip) -> bool:
    try:
        ip_addresses = config('ALLOWED_IPS', default='')
        if ip_addresses == '':
            return True

        iplist = ip_addresses.split(',')
        if host_ip in iplist:
            return True
        else:
            return False
    except Exception as e:
        print(str(e))
        return False


@app.get("/")
async def root():
    return {"message": "Welcome to the sgma-api System."}


@app.middleware("http")
async def before_request(request: Request, call_next):
    try:
        method = request.method
        path = request.url.path
        print(f"method: {method}, path: {path}")
        ip = str(request.client.host)
        if not is_allowed(ip):
            data = {"message": f"IP {ip} is not allowed to access this resource"}
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)
        response = await call_next(request)
    finally:
        pass
    return response
