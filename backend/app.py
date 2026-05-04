from fastapi import FastAPI
from fastapi.responses import JSONResponse
import asyncio
import uvicorn

app = FastAPI(title="F.R.I.D.A.Y. Backend", description="Minimal backend for React frontend integration")

# Estado simulado
system_status = {
    "status": "ok",
    "assistant": "Friday",
    "running": False,
    "message": "System ready"
}

@app.get("/status")
async def get_status():
    """Devuelve el estado actual del sistema"""
    return JSONResponse(content=system_status)

@app.post("/start")
async def start_assistant():
    """Inicia el asistente (simulado)"""
    global system_status
    system_status["running"] = True
    system_status["message"] = "Assistant started"
    return JSONResponse(content={"running": True, "message": "Assistant starting..."})

@app.post("/stop")
async def stop_assistant():
    """Detiene el asistente (simulado)"""
    global system_status
    system_status["running"] = False
    system_status["message"] = "Assistant stopped"
    return JSONResponse(content={"running": False, "message": "Assistant stopped"})

@app.websocket_route("/ws")
async def websocket_endpoint(websocket):
    """WebSocket para eventos en tiempo real (simulado)"""
    await websocket.accept()
    try:
        while True:
            # Enviar evento simulado cada segundo
            await asyncio.sleep(1)
            await websocket.send_json({
                "type": "status_update",
                "data": system_status
            })
    except Exception:
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
