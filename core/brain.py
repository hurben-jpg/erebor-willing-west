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
        
        # Initialize LLM if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        self.llm = None
        if api_key:
            try:
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(api_key=api_key, model="gpt-3.5-turbo")
            except ImportError:
                print("Warning: langchain_openai not installed. Using mock response.")
        else:
            print("Warning: OPENAI_API_KEY not found. Using mock response.")

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
