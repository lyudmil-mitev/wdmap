from sqlalchemy import (
    Column, Integer, String, Float, Date, 
    create_engine
)
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, autoincrement=True)

    full_address = Column(String, index=True)
    longitude = Column(Float, index=True)
    latitude = Column(Float, index=True)
    zip = Column(Integer)

    rec_type = Column(String)
    pin = Column(String, index=True)
    ovacls = Column(String)
    class_description = Column(String)

    current_land = Column(Float)
    current_building = Column(Float)
    current_total = Column(Float)
    estimated_market_value = Column(Float)

    prior_land = Column(Float)
    prior_building = Column(Float)
    prior_total = Column(Float)
    pprior_land = Column(Float)
    pprior_building = Column(Float)
    pprior_total = Column(Float)
    pprior_year = Column(Integer)

    town = Column(String)
    volume = Column(String)
    loc = Column(String)
    tax_code = Column(String)
    neighborhood = Column(String)

    houseno = Column(String)
    dir = Column(String)
    street = Column(String)
    suffix = Column(String)
    apt = Column(String)
    city = Column(String)

    res_type = Column(String)
    bldg_use = Column(String)
    apt_desc = Column(String)
    comm_units = Column(Integer)
    ext_desc = Column(String)
    full_bath = Column(Integer)
    half_bath = Column(Integer)
    bsmt_desc = Column(String)
    attic_desc = Column(String)
    ac = Column(Integer)
    fireplace = Column(Integer)
    gar_desc = Column(String)
    age = Column(Integer)
    building_sq_ft = Column(Integer)
    land_sq_ft = Column(Integer)
    bldg_sf = Column(Integer)
    units_tot = Column(Integer)

    multi_sale = Column(Integer)
    deed_type = Column(String)
    sale_date = Column(Date)
    sale_amount = Column(Float)

    appcnt = Column(Integer)
    appeal_a = Column(String)
    appeal_a_status = Column(String)
    appeal_a_result = Column(String)
    appeal_a_reason = Column(String)
    appeal_a_pin_result = Column(String)
    appeal_a_propav = Column(Float)
    appeal_a_currav = Column(Float)
    appeal_a_resltdate = Column(Date)

engine = create_engine("sqlite:///./properties.db", echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    Base.metadata.create_all(bind=engine)
