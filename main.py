from fastapi import FastAPI, Request
from db import db_route
from parcel import parcel_routes
from wellassoc import wellassoc_routes
from account import account_routes


app = FastAPI()

app.include_router(parcel_routes, prefix="/parcel", tags=["parcel"])
app.include_router(wellassoc_routes, prefix="/well-assoc", tags=["well-assoc"])
app.include_router(account_routes, prefix="/account", tags=["account"])
app.include_router(db_route, prefix="/db", tags=["db"])


@app.get("/")
async def root():
    return {"message": "Welcome to the sgma-api System."}


@app.middleware("http")
async def before_request(request: Request, call_next):
    try:
        method = request.method
        path = request.url.path
        print(f"method: {method}, path: {path}")
        response = await call_next(request)
    finally:
        pass
    return response
