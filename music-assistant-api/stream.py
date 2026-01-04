import uuid
from alexa_state import QUEUES, AlexaQueueState

def get_next_track(queue):
    return {
        "id": "track-1",
        "stream_url": f"https://example.com/stream/{queue}.mp3"
    }

def create_stream(queue, resume, device_id):
    if queue not in QUEUES:
        QUEUES[queue] = AlexaQueueState()

    state = QUEUES[queue]
    state.device_id = device_id

    if not resume or not state.track_id:
        track = get_next_track(queue)
        state.track_id = track["id"]
        state.offset = 0
    else:
        track = get_next_track(queue)

    return {
        "token": str(uuid.uuid4()),
        "url": track["stream_url"],
        "offset": state.offset
    }
