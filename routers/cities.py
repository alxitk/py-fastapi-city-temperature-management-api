from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

import crud
from database import get_db
from models import City
from schema import CityRead, CityCreate


router = APIRouter()

@router.get("/", response_model=list[CityRead])
def get_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db)


@router.post("/create", response_model=CityRead, status_code=201)
def create_city(
        city_data: CityCreate,
        db: Session = Depends(get_db),
):
    return crud.create_city(db, city_data)


@router.delete("/{city_id}", response_model=CityRead)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(City).filter(city_id == City.id).first()

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(city)
    db.commit()
    return city