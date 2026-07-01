import random
from datetime import datetime

class MockSensors:
    def __init__(self):
        self.base_temp = 22.0  # Celsius
        self.base_light = 500  # Lux
        self._overrides = {}

    def update_readings(self, temp: float = None, occupancy: int = None, light: int = None):
        """Manually update sensor readings for testing."""
        if temp is not None:
            self._overrides['temp'] = temp
        if occupancy is not None:
            self._overrides['occupancy'] = occupancy
        if light is not None:
            self._overrides['light'] = light

    def clear_overrides(self):
        """Clear any manual overrides."""
        self._overrides = {}

    def get_temperature(self) -> float:
        """Simulates slight temperature fluctuations."""
        if 'temp' in self._overrides:
            return self._overrides['temp']
        variation = random.uniform(-1.5, 1.5)
        return round(self.base_temp + variation, 1)

    def get_occupancy(self) -> int:
        """Simulates number of people in the building."""
        if 'occupancy' in self._overrides:
            return self._overrides['occupancy']
        # Higher occupancy during day hours (9-17)
        hour = datetime.now().hour
        if 9 <= hour <= 17:
            return random.randint(5, 50)
        return random.randint(0, 5)

    def get_light_level(self) -> int:
        """Simulates light level based on time of day."""
        if 'light' in self._overrides:
            return self._overrides['light']
        hour = datetime.now().hour
        if 6 <= hour <= 18:
            return random.randint(400, 800)  # Daylight
        return random.randint(10, 100)   # Night/Artificial light

    def get_all_readings(self) -> str:
        """Returns a formatted string of all sensor data."""
        temp = self.get_temperature()
        occupancy = self.get_occupancy()
        light = self.get_light_level()
        
        return (
            f"Temperature: {temp}°C\n"
            f"Occupancy: {occupancy} people\n"
            f"Light Level: {light} lux"
        )
