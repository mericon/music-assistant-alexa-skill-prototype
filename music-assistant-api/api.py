from fastapi import FastAPI
from pydantic import BaseModel

from stream import create_stream
from state import handle_state

app = FastAPI()

class StreamReq(BaseModel):
    queue: str
    resume: bool
    device_id: str

class StateReq(BaseModel):
    queue: str
    state: str
    offset: int
    device_id: str

@app.post("/api/alexa/stream")
def stream(req: StreamReq):
    return create_stream(req.queue, req.resume, req.device_id)

@app.post("/api/alexa/state")
def state(req: StateReq):
    handle_state(req.queue, req.state, req.offset, req.device_id)
    return {"status": "ok"}
