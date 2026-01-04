from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_webservice_support.webservice_handler import WebserviceSkillHandler
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_model.interfaces.audioplayer import (
    PlayDirective, PlayBehavior, StopDirective
)

from music_assistant import get_stream, notify_state, get_device_id

sb = SkillBuilder()

class PlayIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        r = handler_input.request_envelope.request
        return r.object_type == "IntentRequest" and r.intent.name == "PlayIntent"

    def handle(self, handler_input):
        device_id = get_device_id(handler_input)
        stream = get_stream(False, device_id)

        return (
            handler_input.response_builder
            .add_directive(
                PlayDirective(
                    play_behavior=PlayBehavior.REPLACE_ALL,
                    audio_item={"stream": stream}
                )
            )
            .response
        )

class PauseHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.object_type == "IntentRequest"

    def handle(self, handler_input):
        return handler_input.response_builder.add_directive(StopDirective()).response

class AudioPlayerEventHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.object_type.startswith("AudioPlayer.")

    def handle(self, handler_input):
        req = handler_input.request_envelope.request
        ctx = handler_input.request_envelope.context
        notify_state(
            req.object_type,
            req.offset_in_milliseconds or 0,
            ctx.system.device.device_id
        )
        return handler_input.response_builder.response

sb.add_request_handler(PlayIntentHandler())
sb.add_request_handler(PauseHandler())
sb.add_request_handler(AudioPlayerEventHandler())

handler = WebserviceSkillHandler(
    skill=sb.create(),
    verify_signature=False,
    verify_timestamp=False
)

if __name__ == "__main__":
    handler.run(host="0.0.0.0", port=8080)
