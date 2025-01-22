import os
import csv
from datetime import datetime
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Property

# Define the path to the data file
current_file_path = os.path.abspath(__file__)
DATA_FILE = os.path.join(os.path.dirname(current_file_path), "..", "data_files", "Enodo_Skills_Assessment_Data_File.csv")

row_labels = [
    ("Full Address", str, "full_address"),
    ("Longitude", float, "longitude"),
    ("Latitude", float, "latitude"),
    ("Zip", int, "zip"),
    ("REC_TYPE", str, "rec_type"),
    ("PIN", str, "pin"),
    ("OVACLS", str, "ovacls"),
    ("CLASS_DESCRIPTION", str, "class_description"),
    ("CURRENT_LAND", float, "current_land"),
    ("CURRENT_BUILDING", float, "current_building"),
    ("CURRENT_TOTAL", float, "current_total"),
    ("ESTIMATED_MARKET_VALUE", float, "estimated_market_value"),
    ("PRIOR_LAND", float, "prior_land"),
    ("PRIOR_BUILDING", float, "prior_building"),
    ("PRIOR_TOTAL", float, "prior_total"),
    ("PPRIOR_LAND", float, "pprior_land"),
    ("PPRIOR_BUILDING", float, "pprior_building"),
    ("PPRIOR_TOTAL", float, "pprior_total"),
    ("PPRIOR_YEAR", int, "pprior_year"),
    ("TOWN", str, "town"),
    ("VOLUME", str, "volume"),
    ("LOC", str, "loc"),
    ("TAX_CODE", str, "tax_code"),
    ("NEIGHBORHOOD", str, "neighborhood"),
    ("HOUSENO", str, "houseno"),
    ("DIR", str, "dir"),
    ("STREET", str, "street"),
    ("SUFFIX", str, "suffix"),
    ("APT", str, "apt"),
    ("CITY", str, "city"),
    ("RES_TYPE", str, "res_type"),
    ("BLDG_USE", str, "bldg_use"),
    ("APT_DESC", str, "apt_desc"),
    ("COMM_UNITS", int, "comm_units"),
    ("EXT_DESC", str, "ext_desc"),
    ("FULL_BATH", int, "full_bath"),
    ("HALF_BATH", int, "half_bath"),
    ("BSMT_DESC", str, "bsmt_desc"),
    ("ATTIC_DESC", str, "attic_desc"),
    ("AC", int, "ac"),
    ("FIREPLACE", int, "fireplace"),
    ("GAR_DESC", str, "gar_desc"),
    ("AGE", int, "age"),
    ("BUILDING_SQ_FT", float, "building_sq_ft"),
    ("LAND_SQ_FT", float, "land_sq_ft"),
    ("BLDG_SF", float, "bldg_sf"),
    ("UNITS_TOT", int, "units_tot"),
    ("MULTI_SALE", int, "multi_sale"),
    ("DEED_TYPE", str, "deed_type"),
    ("SALE_DATE", datetime, "sale_date"),
    ("SALE_AMOUNT", float, "sale_amount"),
    ("APPCNT", int, "appcnt"),
    ("APPEAL_A", str, "appeal_a"),
    ("APPEAL_A_STATUS", str, "appeal_a_status"),
    ("APPEAL_A_RESULT", str, "appeal_a_result"),
    ("APPEAL_A_REASON", str, "appeal_a_reason"),
    ("APPEAL_A_PIN_RESULT", str, "appeal_a_pin_result"),
    ("APPEAL_A_PROPAV", float, "appeal_a_propav"),
    ("APPEAL_A_CURRAV", float, "appeal_a_currav"),
    ("APPEAL_A_RESLTDATE", datetime, "appeal_a_resltdate")
]

def parse_value(value: str, dtype):
    value = value.strip()
    if not value:
        return None

    value = value.replace(",", "")
    try:
        if dtype == datetime:
            return datetime.strptime(value, "%m/%d/%Y")
        return dtype(value)
    except ValueError:
        return None

def fill_db_from_csv():
    db: Session = SessionLocal()

    with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Create a new Property object with parsed fields
            property_obj = Property()
            for label, dtype, attr in row_labels:
                value = row[label]
                if dtype in [int, float, datetime]:
                    value = parse_value(value, dtype)
                else:
                    value = value.strip('"')
                setattr(property_obj, attr, value)
            db.add(property_obj)
        db.commit()
        db.close()


if __name__ == "__main__":
    fill_db_from_csv()
    print("Database successfully populated from CSV.")
