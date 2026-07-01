from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.brain import Brain

app = FastAPI(title="Erebor", description="The Soul of the Building")

# Initialize the Brain
brain = Brain()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    return {"message": "I am Erebor. I am the building."}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = brain.think(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def status():
    return {
        "name": brain.personality.name,
        "address": brain.personality.address,
        "architect": brain.personality.architect,
        "developer": brain.personality.developer,
        "status": brain.personality.config.get("building", {}).get("status", "Under construction"),
        "sensors": brain.sensors.get_all_readings()
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
