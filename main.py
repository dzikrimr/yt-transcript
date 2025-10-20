from fastapi import FastAPI, Query
import httpx

app = FastAPI()

# --- Hardcoded API Key di sini ---
GOOGLE_API_KEY = "AIzaSyCOLyWY92S56k5FVSWlXv0asoVwXKFKq4g"

@app.get("/nearby_places")
async def nearby_places(
    query: str = Query(..., example="rumah sakit Malang"),
    latitude: float = Query(...),
    longitude: float = Query(...)
):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "location": f"{latitude},{longitude}",
        "radius": 5000,  # radius dalam meter
        "key": GOOGLE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

    # Ambil field penting saja
    results = []
    for place in data.get("results", []):
        results.append({
            "id": place.get("place_id"),
            "name": place.get("name"),
            "address": place.get("formatted_address"),
            "lat": place["geometry"]["location"]["lat"],
            "lng": place["geometry"]["location"]["lng"],
            "rating": place.get("rating")
        })

    return {"places": results}
