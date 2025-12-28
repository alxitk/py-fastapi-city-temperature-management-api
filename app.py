from fastapi import FastAPI

from database import Base, engine
from routers import cities, temperatures

app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(cities.router, prefix="/cities", tags=["Cities"])
app.include_router(temperatures.router, prefix="/temperatures", tags=["Temperatures"])