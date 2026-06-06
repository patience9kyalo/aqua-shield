import json
import redis
import httpx
import os
from app.config import config  # Uses your defined config mapping import

class WeatherService:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL")
        
        if redis_url:
            self.redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
        else:
            self.redis_client = redis.Redis(
                host=config.REDIS_HOST, 
                port=config.REDIS_PORT, 
                password=config.REDIS_PASSWORD,
                decode_responses=True,
                ssl=True
            )
            
        self.cache_ttl = 900  # 15 minutes expiration window in seconds

    def _generate_cache_key(self, lat: float, lon: float) -> str:
        return f"weather:forecast:lat_{lat:.2f}:lon_{lon:.2f}"
    
    def _get_mock_data(self, lat: float, lon: float) -> dict:
        # Simulates heavy rainfall parameters to benchmark edge-case aquaculture safety matrices
        return {
            "location": {"lat": lat, "lon": lon, "name": "Simulated Pond Location"},
            "current": {
                "temp_c": 26.5,
                "precip_mm": 12.4,
                "humidity": 85,
                "wind_speed": 15.0
            },
            "forecast": {
                "days": [
                    {"date": "2026-06-05", "avg_temp_c": 25.0, "total_precip_mm": 18.5, "condition": "Heavy Rain"},
                    {"date": "2026-06-06", "avg_temp_c": 27.2, "total_precip_mm": 2.1, "condition": "Partly Cloudy"},
                    {"date": "2026-06-07", "avg_temp_c": 28.0, "total_precip_mm": 0.0, "condition": "Sunny"}
                ]
            }
        }

    async def get_weather_forecast(self, lat: float, lon: float) -> dict:
        cache_key = self._generate_cache_key(lat, lon)

        # Look up memory inside the local tracking grid array
        try:
            cached_data = self.redis_client.get(cache_key)
            if cached_data:
                print(f"--- Cache Hit! Serving instantly from Redis Memory ---")
                return json.loads(cached_data)
        except redis.RedisError as e:
            print(f"Redis cache read error: {e}")

        # Attempt to communicate with the live third-party cloud service
        print(f"Cache miss for key: {cache_key}. Fetching from Weather AI API.")
        url = f"{config.WEATHER_AI_BASE_URL}/forecast"
        params = {"lat": lat, "lon": lon}

        headers = {
            "Authorization": f"Bearer {config.WEATHER_AI_API_KEY}",
            "Accept": "application/json"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    
                    try:
                        self.redis_client.set(cache_key, json.dumps(data), ex=self.cache_ttl)
                    except redis.RedisError as e:
                        print(f"Redis error while setting cache: {e}")
                        
                    return data
                else:
                    print(f"Weather AI API returned status {response.status_code}. Falling back to mock data.")
        except Exception as e:
            print(f"Weather AI API connection failed ({e}). Falling back to mock data.")

        # Fallback handling path
        data = self._get_mock_data(lat, lon)

        try:
            self.redis_client.set(cache_key, json.dumps(data), ex=self.cache_ttl)
        except redis.RedisError as e:
            print(f"Redis error while setting mock cache: {e}")

        return data