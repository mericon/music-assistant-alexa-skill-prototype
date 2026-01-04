import os, requests

MA_BASE_URL = os.getenv("MA_BASE_URL")
MA_API_KEY = os.getenv("MA_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {MA_API_KEY}",
    "Content-Type": "application/json"
}

def get_device_id(handler_input):
    return handler_input.request_envelope.context.system.device.device_id

def get_stream(resume, device_id):
    r = requests.post(
        f"{MA_BASE_URL}/api/alexa/stream",
        headers=HEADERS,
        json={
            "queue": "alexa",
            "resume": resume,
            "device_id": device_id
        }
    )
    r.raise_for_status()
    data = r.json()
    return {
        "token": data["token"],
        "url": data["url"],
        "offset_in_milliseconds": data["offset"]
    }

def notify_state(state, offset, device_id):
    try:
        requests.post(
            f"{MA_BASE_URL}/api/alexa/state",
            headers=HEADERS,
            json={
                "queue": "alexa",
                "state": state,
                "offset": offset,
                "device_id": device_id
            }
        )
    except Exception:
        pass
