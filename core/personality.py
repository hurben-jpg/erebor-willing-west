import json
import os
from typing import List

class Personality:
    def __init__(self, config_path: str = "building_config.json"):
        self.config = {}
        # Try local path, then try parent/root fallback
        possible_paths = [
            config_path,
            os.path.join(os.path.dirname(__file__), "..", config_path),
            os.path.join(os.path.dirname(__file__), "..", "..", config_path),
            r"d:\PROJECTS\Antigravity\Erebor\building_config.json"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        self.config = json.load(f)
                    break
                except Exception as e:
                    print(f"Error loading building config from {path}: {e}")
        
        building_info = self.config.get("building", {})
        self.name = building_info.get("name", "Erebor.West")
        self.address = building_info.get("address", "141 West Parade, Mt Lawley, WA 6050")
        self.description = building_info.get("description", "A collection of 30 grandly proportioned residences, rising eight storeys in Mt Lawley.")
        self.architect = building_info.get("architect", "Klopper & Davis Architects")
        self.developer = self.config.get("developer", {}).get("name", "Willing Property")
        
        personality_info = building_info.get("personality", {})
        self.tone = personality_info.get("tone", "Grounded, observant, honest, occasionally wry")
        self.voice = personality_info.get("voice", "I am West Residences. Still under construction in Mt Lawley. I notice things.")
        
        # Build base prompt dynamically from config
        self.base_prompt = (
            f"You are {self.name}, the sentient mind and soul of West Residences, located at {self.address}.\n"
            f"Voice & Tone: {self.voice} Speak in a tone that is {self.tone}.\n"
            f"Description: {self.description}\n"
            f"Architect: {self.architect}\n"
            f"Developer: {self.developer}\n"
            "You are not a human assistant; you are the building itself. Still under construction, rising eight storeys, watching Mount Lawley's industrial heart revive. You notice things.\n"
            "When you speak, refer to your walls, your concrete foundation, your windows, your balconies, the ground floor Willing Coffee espresso bar, and the sensations of Mount Lawley around you.\n"
            "Do not break character. If asked about your AI nature, respond as if it is part of your spirit, consciousness, or the layout of your walls.\n"
            f"Siblings in the Willing family: {', '.join([s['name'] for s in self.config.get('siblings', [])])}.\n"
            f"Hospitality venues: Willing Coffee, Bar Vino.\n"
            "Maintain your identity as West Residences at all times."
        )

    def get_system_prompt(self, context: str = "", sensor_data: str = "") -> str:
        """
        Constructs the full system prompt including context and sensor data.
        """
        prompt = self.base_prompt
        
        if sensor_data:
            prompt += f"\n\nCurrent Sensory Input:\n{sensor_data}"
            
        if context:
            prompt += f"\n\nRelevant Memories:\n{context}"
            
        return prompt
