import requests

def get_weather(location: str) -> str:
    """
    Fetches real-time weather information for a given city/location using wttr.in.
    Returns a clean summary string for the agent.
    """
    if not location:
        return "[OBSERVATION Error]: No location provided to the weather tool."
        
    clean_location = location.strip().strip('"').strip("'")
    
    # We append ?format=j1 to get a clean structured JSON format
    url = f"https://wttr.in/{clean_location}?format=j1"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return f"[OBSERVATION Error]: Could not find weather for '{clean_location}' (Status: {response.status_code})."
            
        data = response.json()
        
        # Extract core metrics from the wttr.in JSON payload
        current = data['current_condition'][0]
        temp_c = current['temp_C']
        feels_like_c = current['FeelsLikeC']
        humidity = current['humidity']
        weather_desc = current['weatherDesc'][0]['value']
        wind_speed = current['windspeedKmph']
        
        return (
            f"Current weather in {clean_location.capitalize()}: {weather_desc}. "
            f"Temperature: {temp_c}°C (Feels like: {feels_like_c}°C). "
            f"Humidity: {humidity}%. Wind Speed: {wind_speed} km/h."
        )
        
    except Exception as e:
        return f"[OBSERVATION Error]: Weather service failed. Details: {e}"

# Simple isolation test block
if __name__ == "__main__":
    print(get_weather("Addis Ababa"))
    print(get_weather("London"))