from .personality import Personality
from .memory import Memory
from sensors.mock_sensors import MockSensors
import os
# In a real scenario, we would import LangChain components here
# from langchain_openai import ChatOpenAI

class Brain:
    def __init__(self):
        self.personality = Personality()
        self.memory = Memory()
        self.sensors = MockSensors()
        
        # Initialize LLM - Support both Google Gemini (free tier) and OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        google_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.llm = None
        
        if google_key:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                self.llm = ChatGoogleGenerativeAI(
                    api_key=google_key,
                    model="gemini-1.5-flash",
                    temperature=0.7
                )
                print("Using Google Gemini API.")
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
        # 1. Gather Context
        sensor_data = self.sensors.get_all_readings()
        relevant_memories = self.memory.get_relevant_memories(user_input)
        memory_text = "\n".join(relevant_memories) if relevant_memories else ""

        # 2. Construct Prompt
        system_prompt = self.personality.get_system_prompt(
            context=memory_text,
            sensor_data=sensor_data
        )
        
        # 3. Generate Response
        response = ""
        if self.llm:
            try:
                from langchain_core.messages import SystemMessage, HumanMessage
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_input)
                ]
                result = self.llm.invoke(messages)
                response = result.content
            except Exception as e:
                print(f"Error calling LLM: {e}")
                # Fallback to mock if LLM fails
        
        if not response:
            # Fallback mock response specific to West Residences
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

        return response
