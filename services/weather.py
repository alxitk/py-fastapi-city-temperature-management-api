import httpx

async def get_coordinates(city_name: str):
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = r.json()
        if not data:
            return None, None
        return float(data[0]["lat"]), float(data[0]["lon"])


async def fetch_temperature(lat: float, lon: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = r.json()
        return data["current_weather"]["temperature"]