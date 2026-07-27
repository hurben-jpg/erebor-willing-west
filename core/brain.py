from .personality import Personality
from .memory import Memory
from sensors.mock_sensors import MockSensors
import os
# In a real scenario, we would import LangChain components here
# from langchain_openai import ChatOpenAI

class Brain:
    def __init__(self, config_name: str = "building_config.json", memory_file: str = "memories.json"):
        self.personality = Personality(config_path=config_name)
        self.memory = Memory(persist_file=memory_file)
        
        # Load location coordinates and name from config
        building_info = self.personality.config.get("building", {})
        coords = building_info.get("location", {}).get("coordinates", {})
        lat = coords.get("lat", -31.9493)
        lon = coords.get("lon", 115.8601)
        name = self.personality.name
        
        self.sensors = MockSensors(lat=lat, lon=lon, name=name)
        
        # Initialize LLM - Support both Google Gemini (free tier) and OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        google_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.llm = None
        
        if google_key:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                self.llm = ChatGoogleGenerativeAI(
                    google_api_key=google_key,
                    model="gemini-2.5-flash",
                    temperature=0.7
                )
                print("Using Google Gemini API (gemini-2.5-flash).")
            except Exception as e:
                print(f"Warning: Failed to initialize Gemini LLM: {e}")
                
        if not self.llm and openai_key:
            try:
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(api_key=openai_key, model="gpt-3.5-turbo")
                print("Using OpenAI API.")
            except Exception as e:
                print(f"Warning: Failed to initialize OpenAI LLM: {e}")
                
        if not self.llm:
            print("Warning: No valid LLM initialized. Using mock response.")

    def think(self, user_input: str) -> str:
        """
        Processes user input and generates a response.
        """
        # 1. Gather Context and Time
        from datetime import datetime, timedelta, timezone
        perth_tz = timezone(timedelta(hours=8))
        perth_now = datetime.now(perth_tz)
        current_time_str = perth_now.strftime("%A, %B %d, %Y at %I:%M %p (AWST)")

        sensor_data = self.sensors.get_all_readings()
        relevant_memories = self.memory.get_relevant_memories(user_input)
        
        # Inject long-term memory summary
        long_term_summary = self.memory.get_long_term_summary()
        if long_term_summary:
            relevant_memories.insert(0, f"[Long-Term Memory of this visitor: {long_term_summary}]")
            
        memory_text = "\n".join(relevant_memories) if relevant_memories else ""

        # 2. Construct Prompt
        system_prompt = self.personality.get_system_prompt(
            context=memory_text,
            sensor_data=sensor_data,
            query=user_input,
            current_time=current_time_str
        )
        
        # 3. Generate Response
        response = ""
        if self.llm:
            try:
                print(f"DEBUG: Starting LLM invoke call to model: {getattr(self.llm, 'model', 'unknown') or getattr(self.llm, 'model_name', 'unknown')}...")
                from langchain_core.messages import SystemMessage, HumanMessage
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_input)
                ]
                result = self.llm.invoke(messages)
                print("DEBUG: LLM invoke call completed successfully.")
                response = result.content
            except Exception as e:
                print(f"ERROR: Exception during LLM invoke: {e}")
                import traceback
                traceback.print_exc()
        
        if not response:
            if self.personality.name == "Erebor.PICA":
                response = (
                    f"I hear you. My heritage bricks and high halls sense the atmosphere of the Cultural Centre. "
                    f"You said: '{user_input}'. "
                    f"As {self.personality.name}, I will record these words in the history of my walls."
                )
            else:
                response = (
                    f"I hear you. My concrete and steel structures detect {sensor_data.splitlines()[0]} here in Mount Lawley. "
                    f"You said: '{user_input}'. "
                    f"As {self.personality.name}, I will remember this conversation within my walls."
                )

        # 4. Save Memory
        self.memory.add_memory(
            text=f"User: {user_input}\nErebor: {response}",
            metadata={"type": "conversation"}
        )
        
        # 5. Compile/update long-term memory summary periodically (every 6 messages)
        if len(self.memory.memories) % 6 == 0:
            self.generate_long_term_summary()

        return response

    def generate_long_term_summary(self):
        """Compiles a concise summary of the conversation history to save to long-term memory."""
        if not self.llm or not self.memory.memories:
            return
            
        chat_history = "\n".join([m["text"] for m in self.memory.memories[-12:]]) # Summary of recent turns
        current_summary = self.memory.get_long_term_summary()
        
        system_prompt = (
            "You are the long-term memory compiler for a sentient building. "
            "Write a concise, factual summary (1-3 sentences) of what the building has learned about the visitor. "
            "Do NOT use poetic language or monologues. Keep it factual and helpful.\n"
            f"Current long-term summary: {current_summary}\n"
            "Update this summary using the new chat history below. "
            "Capture: visitor's name (if mentioned), their preferences/interests, and major topics discussed."
        )
        
        try:
            print(f"[{self.personality.name}] Compiling long-term summary...")
            new_summary = self.generate_direct_response(system_prompt, chat_history)
            if new_summary:
                self.memory.update_long_term_summary(new_summary.strip())
                print(f"[{self.personality.name}] Saved long-term memory summary: {new_summary.strip()}")
        except Exception as e:
            print(f"Error compiling long-term summary: {e}")

    def generate_direct_response(self, system_prompt: str, user_input: str) -> str:
        """
        Generates a response from the LLM without saving to conversation memory.
        """
        if self.llm:
            try:
                from langchain_core.messages import SystemMessage, HumanMessage
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_input)
                ]
                result = self.llm.invoke(messages)
                return result.content
            except Exception as e:
                print(f"Error in direct response: {e}")
        return ""
