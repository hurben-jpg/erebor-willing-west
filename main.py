from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.brain import Brain

app = FastAPI(title="Erebor", description="The Soul of the Building")

# Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Brain
brain = Brain()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Erebor.West - West Residences Sentient Building</title>
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
      <style>
        :root {
          --bg: #0C0E14;
          --card-bg: rgba(20, 24, 35, 0.6);
          --border: rgba(255, 255, 255, 0.08);
          --accent: #E53935; /* Deli Red */
          --accent-blue: #4DA6E8; /* Deli Blue */
          --text: #FAF6F0; /* Paper White */
          --text-muted: #8E9AA8;
        }
        body {
          margin: 0;
          padding: 0;
          background-color: var(--bg);
          color: var(--text);
          font-family: 'Inter', sans-serif;
          display: flex;
          flex-direction: column;
          height: 100vh;
          overflow: hidden;
        }
        
        /* Subtle micro-pixel mesh overlay */
        body::after {
          content: "";
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-image: 
            linear-gradient(to right, rgba(255, 255, 255, 0.005) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255, 255, 255, 0.005) 1px, transparent 1px);
          background-size: 3px 3px;
          pointer-events: none;
          z-index: 10000;
        }
        
        header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 16px 24px;
          border-bottom: 1px solid var(--border);
          background-color: rgba(12, 14, 20, 0.85);
          backdrop-filter: blur(12px);
          position: relative;
          z-index: 2;
        }
        .header-logo {
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .orb {
          width: 12px;
          height: 12px;
          border-radius: 50%;
          background-color: #4CAF50;
          box-shadow: 0 0 10px #4CAF50;
          animation: pulse 2s infinite;
        }
        @keyframes pulse {
          0% { opacity: 0.6; box-shadow: 0 0 8px #4CAF50; }
          50% { opacity: 1; box-shadow: 0 0 16px #4CAF50; }
          100% { opacity: 0.6; box-shadow: 0 0 8px #4CAF50; }
        }
        .main-layout {
          display: flex;
          flex: 1;
          overflow: hidden;
          position: relative;
          z-index: 2;
        }
        
        /* Sidebar styling */
        .sidebar {
          width: 320px;
          border-right: 1px solid var(--border);
          padding: 24px;
          background-color: rgba(10, 12, 18, 0.5);
          display: flex;
          flex-direction: column;
          gap: 24px;
          overflow-y: auto;
          box-sizing: border-box;
        }
        
        /* Chat window styling */
        .chat-container {
          flex: 1;
          display: flex;
          flex-direction: column;
          background-color: rgba(12, 14, 20, 0.2);
        }
        .chat-history {
          flex: 1;
          padding: 28px;
          overflow-y: auto;
          display: flex;
          flex-direction: column;
          gap: 18px;
          box-sizing: border-box;
        }
        .msg {
          max-width: 75%;
          padding: 14px 20px;
          border-radius: 16px;
          line-height: 1.5;
          font-size: 0.95rem;
          word-wrap: break-word;
          animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .msg.user {
          align-self: flex-end;
          background-color: var(--accent-blue);
          color: #0c0e14;
          font-weight: 500;
          border-bottom-right-radius: 4px;
          box-shadow: 0 4px 12px rgba(77, 166, 232, 0.15);
        }
        .msg.bot {
          align-self: flex-start;
          background-color: rgba(255,255,255,0.03);
          border: 1px solid var(--border);
          color: var(--text);
          border-bottom-left-radius: 4px;
        }
        .input-box {
          padding: 20px 28px;
          border-top: 1px solid var(--border);
          display: flex;
          gap: 14px;
          background-color: rgba(12, 14, 20, 0.9);
          box-sizing: border-box;
        }
        input {
          flex: 1;
          background-color: rgba(255,255,255,0.02);
          border: 1px solid var(--border);
          border-radius: 10px;
          padding: 16px 20px;
          color: var(--text);
          font-family: inherit;
          font-size: 1rem;
          outline: none;
          transition: border-color 0.2s, box-shadow 0.2s;
        }
        input:focus {
          border-color: var(--accent);
          box-shadow: 0 0 0 2px rgba(229, 57, 53, 0.2);
        }
        button {
          background-color: var(--accent);
          color: #fff;
          border: none;
          border-radius: 10px;
          padding: 0 28px;
          font-family: 'Outfit', sans-serif;
          font-weight: 700;
          font-size: 1.05rem;
          cursor: pointer;
          transition: all 0.2s;
          box-shadow: 0 4px 12px rgba(229, 57, 53, 0.3);
        }
        button:hover {
          opacity: 0.95;
          transform: translateY(-1px);
          box-shadow: 0 6px 16px rgba(229, 57, 53, 0.4);
        }
        button:active {
          transform: translateY(0);
        }
        .panel-card {
          background-color: var(--card-bg);
          border: 1px solid var(--border);
          border-radius: 16px;
          padding: 20px;
          backdrop-filter: blur(8px);
        }
        .panel-title {
          font-family: 'Outfit', sans-serif;
          font-size: 0.8rem;
          text-transform: uppercase;
          letter-spacing: 0.12em;
          color: var(--text-muted);
          margin-top: 0;
          margin-bottom: 16px;
          font-weight: 700;
          border-left: 3px solid var(--accent);
          padding-left: 8px;
        }
        .stat-row {
          display: flex;
          justify-content: space-between;
          margin-bottom: 12px;
          font-size: 0.9rem;
          border-bottom: 1px dashed rgba(255,255,255,0.03);
          padding-bottom: 8px;
        }
        .stat-row:last-child {
          margin-bottom: 0;
          border-bottom: none;
          padding-bottom: 0;
        }
        .stat-label {
          color: var(--text-muted);
        }
        .stat-val {
          font-weight: 600;
          color: var(--text);
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
          width: 6px;
        }
        ::-webkit-scrollbar-track {
          background: transparent;
        }
        ::-webkit-scrollbar-thumb {
          background: rgba(255,255,255,0.05);
          border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
          background: rgba(255,255,255,0.1);
        }
      </style>
    </head>
    <body>
      <header>
        <div class="header-logo">
          <div class="orb"></div>
          <h1 style="margin:0; font-family:'Outfit', sans-serif; font-size:1.35rem; font-weight:800; letter-spacing:0.08em; color:#fff;">EREBOR.WEST</h1>
        </div>
        <div style="font-family:'Outfit', sans-serif; font-size:0.75rem; color:var(--text-muted); letter-spacing:0.05em; font-weight:600; text-transform:uppercase;">Mt Lawley Sentient System</div>
      </header>
      
      <div class="main-layout">
        <div class="sidebar">
          <div class="panel-card">
            <h3 class="panel-title">Environmental Telemetry</h3>
            <div id="sensor-telemetry">
              <div style="color:var(--text-muted); font-size:0.85rem; font-style:italic;">Loading sensory array...</div>
            </div>
          </div>
          
          <div class="panel-card">
            <h3 class="panel-title">Structure Parameters</h3>
            <div class="stat-row"><span class="stat-label">Identity:</span><span class="stat-val" id="spec-name">-</span></div>
            <div class="stat-row"><span class="stat-label">Address:</span><span class="stat-val" id="spec-address" style="text-align:right; font-size:0.85rem;">-</span></div>
            <div class="stat-row"><span class="stat-label">Architecture:</span><span class="stat-val" id="spec-architect">-</span></div>
            <div class="stat-row"><span class="stat-label">Developer:</span><span class="stat-val" id="spec-developer">-</span></div>
            <div class="stat-row"><span class="stat-label">Status:</span><span class="stat-val" id="spec-status" style="font-size:0.85rem; text-align:right;">-</span></div>
          </div>
        </div>
        
        <div class="chat-container">
          <div class="chat-history" id="chat-history">
            <div class="msg bot">I am the mind of West Residences. Speak to me. I observe Mt Lawley from my emerging eight storeys.</div>
          </div>
          <div class="input-box">
            <input type="text" id="chat-input" placeholder="Transmit a message to the walls..." autocomplete="off">
            <button id="send-btn">Speak</button>
          </div>
        </div>
      </div>
      
      <script>
        const chatHistory = document.getElementById('chat-history');
        const chatInput = document.getElementById('chat-input');
        const sendBtn = document.getElementById('send-btn');
        
        async function loadStatus() {
          try {
            const res = await fetch('/status');
            const data = await res.json();
            document.getElementById('spec-name').textContent = data.name || '-';
            document.getElementById('spec-address').textContent = data.address || '-';
            document.getElementById('spec-architect').textContent = data.architect || '-';
            document.getElementById('spec-developer').textContent = data.developer || '-';
            document.getElementById('spec-status').textContent = data.status || '-';
            
            const sensors = data.sensors.split('\\n');
            let sensorHtml = '';
            sensors.forEach(s => {
              const parts = s.split(': ');
              if (parts.length === 2) {
                sensorHtml += `<div class="stat-row"><span class="stat-label">${parts[0]}:</span><span class="stat-val">${parts[1]}</span></div>`;
              }
            });
            document.getElementById('sensor-telemetry').innerHTML = sensorHtml || data.sensors;
          } catch (e) {
            console.error('Failed to load status', e);
          }
        }
        
        async function handleSend() {
          const text = chatInput.value.trim();
          if (!text) return;
          
          appendMsg(text, 'user');
          chatInput.value = '';
          
          const thinkingDiv = appendMsg('Concrete circuits aligning...', 'bot');
          
          try {
            const res = await fetch('/chat', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ message: text })
            });
            const data = await res.json();
            thinkingDiv.textContent = data.response;
          } catch (e) {
            thinkingDiv.textContent = 'I cannot reach my mind... (Network Error)';
          }
          
          chatHistory.scrollTop = chatHistory.scrollHeight;
        }
        
        function appendMsg(text, sender) {
          const div = document.createElement('div');
          div.className = `msg ${sender}`;
          div.textContent = text;
          chatHistory.appendChild(div);
          chatHistory.scrollTop = chatHistory.scrollHeight;
          return div;
        }
        
        sendBtn.addEventListener('click', handleSend);
        chatInput.addEventListener('keydown', (e) => {
          if (e.key === 'Enter') handleSend();
        });
        
        loadStatus();
        setInterval(loadStatus, 10000);
      </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

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
