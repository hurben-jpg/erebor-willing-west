# Technical Design: Erebor

## System Architecture

### 1. Core Brain (`core/brain.py`)
- **Role**: Orchestrates the AI's thought process.
- **Components**:
    - `Personality`: Manages the system prompt and character traits.
    - `Memory`: Interfaces with the Vector DB to retrieve context.
    - `Sensors`: Aggregates data from the sensor module.
- **Flow**: Input -> Retrieve Context -> Read Sensors -> Generate Response -> Save Context.

### 2. Memory Module (`core/memory.py`)
- **Technology**: ChromaDB (Local).
- **Schema**:
    - `content`: The message/interaction text.
    - `metadata`: Timestamp, speaker (User/Erebor), tags.
- **Functionality**:
    - `add_memory(text, metadata)`
    - `get_relevant_memories(query)`

### 3. Sensor Module (`sensors/`)
- **Role**: Provide environmental context.
- **Interface**:
    - `get_temperature()`
    - `get_occupancy()`
    - `get_light_level()`
- **Implementation**: Initially mock data, designed to be swappable for real IoT inputs.

### 4. API Layer (`main.py`)
- **Framework**: FastAPI.
- **Endpoints**:
    - `POST /chat`: User interacts with Erebor.
    - `GET /status`: View Erebor's current "mood" and sensor readings.

## Data Flow
1. User sends message to `/chat`.
2. API handler passes message to `Brain`.
3. `Brain` queries `Memory` for related past interactions.
4. `Brain` polls `Sensors` for current state (e.g., "It's cold outside").
5. `Brain` constructs a prompt with:
    - System Personality
    - Relevant Memories
    - Current Sensor Data
    - User Message
6. LLM generates response.
7. Response is saved to `Memory`.
8. Response returned to User.
