import pytest
import shutil
import os
import sys
from unittest.mock import MagicMock

# Mock chromadb before importing core modules
sys.modules["chromadb"] = MagicMock()
sys.modules["chromadb.config"] = MagicMock()

from core.brain import Brain
from core.memory import Memory
from sensors.mock_sensors import MockSensors

# Test Memory
def test_memory_add_and_retrieve():
    # Use a temporary directory for testing
    test_db_path = "./test_chroma_db"
    if os.path.exists(test_db_path):
        shutil.rmtree(test_db_path)
        
    memory = Memory(persist_directory=test_db_path)
    
    # Configure mock to return data
    mock_collection = memory.collection
    mock_collection.query.return_value = {
        'documents': [["User: Hello"]]
    }
    
    # Add a memory
    memory.add_memory("User: Hello", {"type": "test"})
    
    # Retrieve it
    results = memory.get_relevant_memories("Hello")
    assert len(results) > 0
    assert "User: Hello" in results[0]
    
    # Cleanup
    if os.path.exists(test_db_path):
        shutil.rmtree(test_db_path)

# Test Sensors
def test_sensor_overrides():
    sensors = MockSensors()
    
    # Default behavior (random)
    temp = sensors.get_temperature()
    assert 20.5 <= temp <= 23.5
    
    # Override behavior
    sensors.update_readings(temp=30.0, occupancy=100, light=10)
    assert sensors.get_temperature() == 30.0
    assert sensors.get_occupancy() == 100
    assert sensors.get_light_level() == 10
    
    # Clear overrides
    sensors.clear_overrides()
    temp = sensors.get_temperature()
    assert 20.5 <= temp <= 23.5

# Test Brain (Mock LLM)
def test_brain_think_mock():
    # Ensure no API key is set for this test to force mock
    original_key = os.environ.get("OPENAI_API_KEY")
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
        
    brain = Brain()
    
    # Set sensor values to known state
    brain.sensors.update_readings(temp=25.0)
    
    response = brain.think("Hello Erebor")
    
    # Check response contains sensor data
    assert "25.0" in response
    assert "Hello Erebor" in response
    
    # Restore API key if it existed
    if original_key:
        os.environ["OPENAI_API_KEY"] = original_key
