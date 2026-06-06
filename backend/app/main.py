import os

from fastapi import FastAPI, HTTPException
import uvicorn
from app.services import WeatherService
from fastapi.middleware.cors import CORSMiddleware
from app.utils import PondMetricsEngine 

app = FastAPI(title="Aqua Shield Weather Backend")

# CORS configuration to allow frontend access

origin = [
    "http://localhost:5173",
    "https://aqua-shield-drab.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

weather_service = WeatherService()


@app.get("/")
def read_root():
    return {"status": "healthy", "service": "Aqua Shield Weather Backend"}


@app.get("/api/weather")
async def get_weather_insights(lat: float, lon: float, base_feed_kg: float = 50.0):
    try:
        # 1. Fetch live data from your service (which hits the API or Redis)
        raw_weather = await weather_service.get_weather_forecast(lat, lon)

        # 2. KEY MAPPING LAYER (Normalizes real API keys to match utils_4.py)
        if "current" in raw_weather:
            current = raw_weather["current"]
            
            # Map temperature key if the API uses 'temperature' instead of 'temp_c'
            if "temp_c" not in current and "temperature" in current:
                current["temp_c"] = current.get("temperature")
                
            # Map humidity key if the API uses a different variation
            if "humidity" not in current and "humidity_percentage" in current:
                current["humidity"] = current.get("humidity_percentage")
                
            # Map precipitation key if needed
            if "precip_mm" not in current and "precipitation" in current:
                current["precip_mm"] = current.get("precipitation")

        # 3. Pass the freshly aligned data into your engine
        analytics_payload = PondMetricsEngine.process_air_to_pond_analytics(
            raw_weather, base_feed_kg=base_feed_kg
        )

        return analytics_payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)