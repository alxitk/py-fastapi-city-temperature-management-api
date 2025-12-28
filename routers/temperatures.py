from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

import crud
from database import get_db
from schema import CityRead, TemperatureRead
from services.weather import get_coordinates, fetch_temperature

router = APIRouter()

@router.post("/update")
async def update_temperature(db: Session = Depends(get_db)):
    cities = crud.get_all_cities(db)

    for city in cities:
        lat, lon = await get_coordinates(city.name)
        if lat is None or lon is None:
            continue

        temp = await fetch_temperature(lat, lon)
        crud.save_temperature(db, city.id, temp)
        db.commit()
    return {"status": "success"}


@router.get("/", response_model=list[TemperatureRead])
async def get_temperature(db: Session = Depends(get_db)):
    return crud.get_temperature_list(db)


@router.get("/{city_id}")
async def get_city_temperature(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city_by_id(city_id, db)

    temps = crud.get_city_temperature_list(db, city.id)
    return temps