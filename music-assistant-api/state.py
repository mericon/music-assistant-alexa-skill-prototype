from alexa_state import QUEUES

def handle_state(queue, state, offset, device_id):
    q = QUEUES.get(queue)
    if not q:
        return

    if state.endswith("PlaybackStopped"):
        q.offset = offset
        q.playing = False
    elif state.endswith("PlaybackStarted"):
        q.playing = True
    elif state.endswith("PlaybackFinished"):
        q.offset = 0
        q.track_id = None
        q.playing = False
