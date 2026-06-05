class PondMetricsEngine:
    @staticmethod
    def evaluate_thermal_conditions(temp_c: float) -> dict:
        # Evaluates how current air temperature affects fish metabolism and feeding behavior.
        
        if temp_c is None:
            return {"status": "UNKNOWN", "message": "Thermal data unavailable.", "feeding_multiplier": 1.0}
            
        if 24.0 <= temp_c <= 30.0:
            return {
                "status": "OPTIMAL",
                "message": f"Air temperature ({temp_c}°C) is excellent for pond metabolic activity.",
                "feeding_multiplier": 1.0
            }
        elif 20.0 <= temp_c < 24.0:
            return {
                "status": "WARNING_LOW",
                "message": f"Cooler air temperature ({temp_c}°C) may slightly decrease feeding activity.",
                "feeding_multiplier": 0.8
            }
        elif temp_c > 30.0:
            return {
                "status": "WARNING_HIGH",
                "message": f"Elevated temperature ({temp_c}°C) reduces dissolved oxygen solubility. Monitor aeration.",
                "feeding_multiplier": 0.75
            }
        else:
            return {
                "status": "CRITICAL_LOW",
                "message": f"Critical low temperature ({temp_c}°C). Dramatically reduce feeding to prevent waste decay.",
                "feeding_multiplier": 0.5
            }

    @staticmethod
    def evaluate_hydrology_risk(current_precip_mm: float, forecast_days: list) -> dict:
        # Assesses risk of pond overflow based on current precipitation and cumulative forecasted rainfall.

        current_precip = current_precip_mm or 0.0
        forecast_precip_total = sum(day.get("total_precip_mm", 0.0) for day in forecast_days) if forecast_days else 0.0
        cumulative_rainfall = current_precip + forecast_precip_total

        if cumulative_rainfall >= 30.0:
            return {
                "risk_level": "HIGH",
                "cumulative_predicted_rainfall_mm": round(cumulative_rainfall, 2),
                "action_required": "CRITICAL: High overflow risk! Clear emergency spillways and secure freeboard drainage screens."
            }
        elif 15.0 <= cumulative_rainfall < 30.0:
            return {
                "risk_level": "MEDIUM",
                "cumulative_predicted_rainfall_mm": round(cumulative_rainfall, 2),
                "action_required": "MONITOR: Moderate rain volume. Ensure outflow pipes are clear of debris."
            }
        else:
            return {
                "risk_level": "LOW",
                "cumulative_predicted_rainfall_mm": round(cumulative_rainfall, 2),
                "action_required": "ROUTINE: Normal operations. Structural hydrology limits are safe."
            }

    @staticmethod
    def predict_dissolved_oxygen_risk(temp_c: float, wind_speed: float) -> dict:
        # Predicts risk of dissolved oxygen depletion based on current temperature and wind speed, which affect oxygen diffusion rates.

        if temp_c is None or wind_speed is None:
            return {"risk_level": "LOW", "message": "Insufficient atmospheric metrics for DO tracking."}

        # Stagnation factor if wind speed is below 5 kph
        is_stagnant = wind_speed < 5.0
        
        if temp_c > 30.0 and is_stagnant:
            return {
                "risk_level": "CRITICAL",
                "message": f"CRITICAL: Extreme heat ({temp_c}°C) and stagnant air ({wind_speed} kph) detected. Run mechanical aerators immediately to prevent overnight fish kill."
            }
        elif temp_c > 28.0 or is_stagnant:
            return {
                "risk_level": "MEDIUM",
                "message": "WARNING: Moderate risk of dissolved oxygen drop. Keep a close eye on fish surface activity during dawn."
            }
        
        return {
            "risk_level": "LOW",
            "message": "Dissolved oxygen diffusion rates are stable under current atmospheric mixing."
        }

    @staticmethod
    def calculate_optimized_feed_ration(base_daily_ration_kg: float, multiplier: float) -> dict:
        # Calculates optimized feed ration based on thermal conditions. Reduces feed during suboptimal temperatures to prevent waste and water quality degradation.

        optimized_ration = base_daily_ration_kg * multiplier
        savings_g = (base_daily_ration_kg - optimized_ration) * 1000

        return {
            "recommended_feed_kg": round(optimized_ration, 2),
            "adjustment_applied": f"{int(multiplier * 100)}%",
            "feed_saved_g": round(savings_g, 2) if savings_g > 0 else 0.0
        }

    @classmethod
    def process_air_to_pond_analytics(cls, weather_payload: dict, base_feed_kg: float = 50.0) -> dict:
        # Transforms raw weather data into actionable insights for pond management. Integrates thermal, hydrological, and oxygen risk assessments to provide a comprehensive action plan.

        current = weather_payload.get("current", {})
        forecast = weather_payload.get("forecast", {})
        location = weather_payload.get("location", {})

        current_temp = current.get("temp_c")
        current_precip = current.get("precip_mm", 0.0)
        current_wind = current.get("wind_speed", 0.0)
        forecast_days = forecast.get("days", [])

        # Run subsystems
        thermal = cls.evaluate_thermal_conditions(current_temp)
        hydrology = cls.evaluate_hydrology_risk(current_precip, forecast_days)
        oxygen = cls.predict_dissolved_oxygen_risk(current_temp, current_wind)
        feeding = cls.calculate_optimized_feed_ration(base_feed_kg, thermal["feeding_multiplier"])

        return {
            "meta": {
                "location_name": location.get("name", "Active Coordinate Grid"),
                "latitude": location.get("lat"),
                "longitude": location.get("lon")
            },
            "atmospheric_snapshot": {
                "temperature_c": current_temp,
                "precipitation_mm": current_precip,
                "humidity_percentage": current.get("humidity"),
                "wind_speed": current_wind
            },
            "aquaculture_insights": {
                "thermal_management": thermal,
                "hydrology_safety": hydrology,
                "dissolved_oxygen_risk": oxygen,
                "feed_optimization": feeding,
                "action_plan": [
                    thermal["message"],
                    hydrology["action_required"],
                    oxygen["message"]
                ]
            }
        }