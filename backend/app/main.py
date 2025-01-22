from fastapi import FastAPI, Depends, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import get_db
from .models import Property

app = FastAPI()
# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "Welcome to the Property API"}

@app.get("/properties")
def list_properties(
    db: Session = Depends(get_db),
    limit: int = 10,
    offset: int = 0,
    full_address: str = Query(None),
    class_description: str = Query(None),
    min_market_value: float = Query(None),
    max_market_value: float = Query(None)
):
    query = db.query(Property)
    
    print(f"full_address: {full_address}, limit: {limit}, offset: {offset}")
    if full_address:
        query = query.filter(Property.full_address.contains(full_address))
    if class_description:
        query = query.filter(Property.class_description.contains(class_description))
    if min_market_value is not None:
        query = query.filter(Property.estimated_market_value >= min_market_value)
    if max_market_value is not None:
        query = query.filter(Property.estimated_market_value <= max_market_value)

    # Pagination
    query = query.offset(offset).limit(limit)

    return query.all()

@app.get("/properties/{property_id}")
def get_property_by_id(property_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single property by its database ID.
    """
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Property with ID {property_id} not found."
        )
    return prop