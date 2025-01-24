from fastapi import FastAPI, Depends, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from pydantic import conint
from .database import get_db
from .models import Property
import secrets

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    # TODO: Set the hardcoded username and password in .env instead
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "admin")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return {"message": "Login successful"}


@app.get("/")
def root(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return {"message": "Welcome to the Property API"}


@app.get("/properties")
def list_properties(
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(verify_credentials),
    limit: conint(ge=0, le=1500) = 10, # Set maximum for limit to 1500
    offset: conint(ge=0) = 0, # Set minimum for offset to 0
    full_address: str = Query(None),
    class_description: str = Query(None),
    estimated_market_value: str = Query(None, pattern=r"^\d+,\d+$"),
    building_sq_ft: str = Query(None, pattern=r"^\d+,\d+$"),
    bldg_use: str = Query(None),
):
    query = db.query(Property)

    if full_address:
        query = query.filter(Property.full_address.contains(full_address))

    if class_description:
        query = query.filter(Property.class_description.contains(class_description))

    if estimated_market_value:
        low, high = estimated_market_value.split(",")
        query = query.filter(Property.estimated_market_value >= low)
        query = query.filter(Property.estimated_market_value <= high)

    if building_sq_ft:
        low, high = building_sq_ft.split(",")
        query = query.filter(Property.building_sq_ft >= low)
        query = query.filter(Property.building_sq_ft <= high)

    if bldg_use:
        for use in bldg_use.split(","):
            query = query.filter(Property.bldg_use.contains(use))

    # Pagination
    query = query.offset(offset).limit(limit)

    return query.all()


@app.get("/properties/{property_id}")
def get_property_by_id(
    property_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(verify_credentials),
):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Property with ID {property_id} not found.",
        )
    return prop


@app.get("/all_properties")
def list_property_coordinates(
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(verify_credentials),
):
    properties = db.query(Property.id, Property.latitude, Property.longitude).all()
    return [
        {"id": prop.id, "latitude": prop.latitude, "longitude": prop.longitude}
        for prop in properties
    ]
