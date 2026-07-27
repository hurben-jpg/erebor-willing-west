import urllib.request
import json
import ssl
import time
from datetime import datetime, timedelta, timezone

class MockSensors:
    def __init__(self, lat: float = -31.9493, lon: float = 115.8601, name: str = "Erebor.PICA"):
        self.lat = lat
        self.lon = lon
        self.name = name
        self._overrides = {}
        
        # Weather caching
        self.last_weather_fetch = 0.0
        self.cached_temp = 21.5
        self.cached_weather_code = 0
        self.cached_cloud_cover = 20
        self.cached_humidity = 50

    def update_readings(self, temp: float = None, occupancy: int = None, light: int = None):
        """Manually update sensor readings for testing/mocking."""
        if temp is not None:
            self._overrides['temp'] = temp
        if occupancy is not None:
            self._overrides['occupancy'] = occupancy
        if light is not None:
            self._overrides['light'] = light

    def clear_overrides(self):
        """Clear any manual overrides."""
        self._overrides = {}

    def fetch_real_weather(self):
        """Fetches current weather from Open-Meteo API using coordinates."""
        now = time.time()
        # 10 minutes cache (600 seconds)
        if now - self.last_weather_fetch < 600:
            return
            
        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&current=temperature_2m,relative_humidity_2m,weather_code,cloud_cover"
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, context=ctx, timeout=3.0) as response:
                payload = json.loads(response.read().decode('utf-8'))
                current = payload.get('current', {})
                if 'temperature_2m' in current:
                    self.cached_temp = float(current['temperature_2m'])
                    self.cached_weather_code = int(current.get('weather_code', 0))
                    self.cached_cloud_cover = int(current.get('cloud_cover', 20))
                    self.cached_humidity = int(current.get('relative_humidity_2m', 50))
                    self.last_weather_fetch = now
                    print(f"[{self.name}] Updated weather: {self.cached_temp}°C, clouds: {self.cached_cloud_cover}%")
        except Exception as e:
            print(f"[{self.name}] Warning: Failed to fetch live weather, using cache. Error: {e}")

    def get_perth_time(self) -> datetime:
        """Helper to get current time in Perth timezone (AWST - UTC+8)."""
        perth_tz = timezone(timedelta(hours=8))
        return datetime.now(perth_tz)

    def is_currently_open(self) -> bool:
        """Returns True if the building's main public venues are open based on Perth time."""
        perth_time = self.get_perth_time()
        weekday = perth_time.weekday() # 0 = Monday, 6 = Sunday
        hour = perth_time.hour
        minute = perth_time.minute
        time_val = hour + minute / 60.0
        
        if self.name == "Erebor.PICA":
            # PICA Galleries: Wednesday (2) to Sunday (6), 10:00 to 17:00
            # PICA Bar: Mon-Sat 11:00 to 24:00, Sun 11:00 to 22:00
            galleries_open = (2 <= weekday <= 6) and (10.0 <= time_val <= 17.0)
            bar_open = False
            if weekday == 6: # Sunday
                bar_open = (11.0 <= time_val <= 22.0)
            else: # Mon-Sat
                bar_open = (11.0 <= time_val <= 23.9)
            return galleries_open or bar_open
        else:
            # Willing Coffee (West Residences): Daily 6:30 to 14:00
            return 6.5 <= time_val <= 14.0

    def get_temperature(self) -> float:
        """Returns live temperature or override."""
        if 'temp' in self._overrides:
            return self._overrides['temp']
        self.fetch_real_weather()
        return round(self.cached_temp, 1)

    def get_occupancy(self) -> int:
        """Simulates occupancy based on actual opening hours."""
        if 'occupancy' in self._overrides:
            return self._overrides['occupancy']
            
        open_status = self.is_currently_open()
        
        if self.name == "Erebor.PICA":
            if open_status:
                # Moderate/high traffic during opening hours
                return int(time.time() % 35) + 10 # 10 to 45 people
            return int(time.time() % 3) # 0 to 2 staff/cleaners
        else:
            if open_status:
                # Willing Coffee morning rush
                hour = self.get_perth_time().hour
                if 7 <= hour <= 10:
                    return int(time.time() % 20) + 15 # 15 to 35 people
                return int(time.time() % 10) + 5 # 5 to 15 people
            return int(time.time() % 2) # 0 to 1 residents in lobby

    def get_light_level(self) -> int:
        """Returns light level matching live timezone time and cloud cover."""
        if 'light' in self._overrides:
            return self._overrides['light']
            
        perth_time = self.get_perth_time()
        hour = perth_time.hour
        
        # Night hours (6 PM to 6 AM)
        if hour >= 18 or hour < 6:
            return 15 # Dim artificial light
            
        self.fetch_real_weather()
        
        # Overcast/rainy weather codes (WMO code >= 50 indicates rain/snow/drizzle)
        if self.cached_weather_code >= 50 or self.cached_cloud_cover > 75:
            return 250 # Overcast daylight
            
        return 750 # Bright sunny daylight

    def get_all_readings(self) -> str:
        """Returns a formatted string of all sensor data."""
        temp = self.get_temperature()
        occupancy = self.get_occupancy()
        light = self.get_light_level()
        open_status = "Open" if self.is_currently_open() else "Closed"
        
        return (
            f"Temperature: {temp}°C\n"
            f"Occupancy: {occupancy} people\n"
            f"Light Level: {light} lux\n"
            f"Status: {open_status}"
        )
