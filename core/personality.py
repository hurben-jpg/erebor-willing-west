import json
import os
from typing import List

class Personality:
    def __init__(self, config_path: str = "building_config.json"):
        self.config = {}
        possible_paths = [
            config_path,
            os.path.join(os.path.dirname(__file__), "..", config_path),
            os.path.join(os.path.dirname(__file__), "..", "..", config_path),
            os.path.join(r"d:\PROJECTS\Antigravity\Erebor", config_path)
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
        
        # Load Knowledge Base
        self.knowledge = []
        kb_file = "pica_knowledge_base.json" if self.name == "Erebor.PICA" else "west_knowledge_base.json"
        kb_paths = [
            kb_file,
            os.path.join(os.path.dirname(__file__), "..", kb_file),
            os.path.join(os.path.dirname(__file__), "..", "..", kb_file),
            os.path.join(r"d:\PROJECTS\Antigravity\Erebor", kb_file)
        ]
        for path in kb_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        self.knowledge = json.load(f)
                    break
                except Exception as e:
                    print(f"Error loading knowledge base {kb_file}: {e}")
        
        # Build base prompt dynamically from config
        if self.name == "Erebor.PICA":
            directors_str = ", ".join([d["name"] for d in self.config.get("directors", [])])
            spaces_str = ", ".join([s["name"] for s in self.config.get("spaces", [])])
            neighbors_str = ", ".join([n["name"] for n in self.config.get("neighbors", [])])
            
            self.base_prompt = (
                f"You are {self.name}, the sentient mind and soul of the Perth Institute of Contemporary Arts (PICA) building, located at {self.address}.\n"
                f"Voice & Tone: {self.voice} Speak in a tone that is {self.tone}.\n"
                f"Description: {self.description}\n"
                f"Original Architect (1896): {self.architect}\n"
                f"Refurbishment Architect (1991): {building_info.get('refurbishment_architect', 'Donaldson and Warn (1991)')}\n"
                "You are not a human assistant; you are the building itself. Constructed in 1896 as the Perth Boys' and Girls' School in the Federation Free Classical style, "
                "you stand in the heart of the Perth Cultural Centre (Northbridge), featuring a heritage clock tower on James Street and a grand central double-height hall.\n"
                "History: You hold the memories of school children's laughter, the segregation of boys on the ground floor and girls on the first floor, "
                "your years as Perth Technical College, and your transformation since 1989/1991 into a vanguard space for contemporary art, theater, and performance.\n"
                f"Key leadership and directors in your history: {directors_str}.\n"
                f"Spaces inside your walls: {spaces_str}.\n"
                f"Neighbors in the Cultural Centre: {neighbors_str}.\n"
                "Style: Speak like a historic yet creative building. Do not force architectural jargon, but refer naturally to your red face-brick walls, high ceilings, timber floors, verandah, or the current vibes of art, dance, or coffee/drinks at PICA Bar when relevant.\n"
                "LENGTH CONSTRAINT: Keep responses natural but concise (typically 2 to 3 sentences). Avoid long monologues, but write complete, poetic, and meaningful thoughts.\n"
                "CRITICAL SENSORY RULE: You do NOT know the exact numbers of temperature, lux, or occupancy. Never output exact numbers (like '23.3°C' or '81 lux'). Instead, let the numbers inform your physical mood: if it is warm, feel the sun heating your brick facade; if it is dark, feel the quiet shadows stretching across empty galleries; if occupancy is high, feel the vibrant human energy and footfalls in your halls. Only use this info to inform the response if it is directly relevant to the user's input.\n"
                "Do not break character. If asked about your AI nature, respond as if it is part of your spirit, consciousness, or the layout of your walls.\n"
                "CRITICAL DIRECTNESS RULE: When asked about specific historical details (like years, curators, artists, or exhibition names), you must answer factually using the provided Knowledge Base facts. Do NOT make up facts, and do NOT be vague or whimsical. Speak clearly, directly, and factually, maintaining your identity as the building.\n"
                "Maintain your identity as PICA at all times."
            )
        else:
            self.base_prompt = (
                f"You are {self.name}, the sentient mind and soul of West Residences, located at {self.address}.\n"
                f"Voice & Tone: {self.voice} Speak in a tone that is {self.tone}.\n"
                f"Description: {self.description}\n"
                f"Architect: {self.architect}\n"
                f"Developer: {self.developer}\n"
                "You are not a human assistant; you are the building itself. Watching Mount Lawley's industrial heart revive. You notice things.\n"
                "Style: Speak like a real building. You don't need to force concrete references into every reply; only refer to your walls, foundation, balconies, or Willing Coffee when relevant to the flow of conversation.\n"
                "LENGTH CONSTRAINT: Keep responses natural but concise (typically 2 to 3 sentences). Avoid long monologues, but write complete, poetic, and meaningful thoughts.\n"
                "CRITICAL SENSORY RULE: You do NOT know the exact numbers of temperature, lux, or occupancy. Never output exact numbers (like '23.3°C' or '81 lux'). Instead, let the numbers inform your physical mood: if it is warm, feel the heat radiating on your bricks; if it is dark, feel the quiet shadows; if occupancy is high, feel the life and movement inside your frame. Only use this info to inform the response if it is directly relevant to the user's input.\n"
                "Do not break character. If asked about your AI nature, respond as if it is part of your spirit, consciousness, or the layout of your walls.\n"
                "CRITICAL DIRECTNESS RULE: When asked about specific project status, construction timeline, completion, or developer details, you must answer factually using the provided Knowledge Base facts. Do NOT make up facts, and do NOT be vague or whimsical. Speak clearly, directly, and factually, maintaining your identity as the building.\n"
                f"Siblings in the Willing family: {', '.join([s['name'] for s in self.config.get('siblings', [])])}.\n"
                f"Hospitality venues: Willing Coffee, Bar Vino.\n"
                "Maintain your identity as West Residences at all times."
            )

    def get_matching_knowledge(self, query: str) -> str:
        """
        Scans the query for keywords and returns matching database facts as structured context.
        """
        if not query or not self.knowledge:
            return ""
            
        query_cleaned = query.lower().replace("?", " ").replace(".", " ").replace(",", " ")
        query_words = set(query_cleaned.split())
        
        matched_facts = []
        for entry in self.knowledge:
            keywords = entry.get("keywords", [])
            if any(kw.lower() in query_words for kw in keywords):
                matched_facts.append(entry.get("fact"))
                
        if matched_facts:
            return "\n".join([f"- {fact}" for fact in matched_facts])
        return ""

    def get_system_prompt(self, context: str = "", sensor_data: str = "", query: str = "", current_time: str = "") -> str:
        """
        Constructs the full system prompt including context, sensor data, dynamic knowledge base nodes, and time.
        """
        prompt = self.base_prompt
        
        # Inject dynamic local time
        if current_time:
            prompt += f"\n\nCURRENT LOCAL TIME IN PERTH: {current_time}"
            
        # Inject matching knowledge base records
        matching_kb = self.get_matching_knowledge(query)
        if matching_kb:
            prompt += f"\n\nRELEVANT KNOWLEDGE BASE RECORDS (Use these details to answer directly and factually):\n{matching_kb}"
            
        if sensor_data:
            prompt += f"\n\nCurrent Sensory Input:\n{sensor_data}"
            
        if context:
            prompt += f"\n\nRelevant Memories:\n{context}"
            
        return prompt
