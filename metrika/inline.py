from commands.inline_add_counter import InlineAddCounter
from commands.subscribe import CommandSubscribe

class InlineCommandsHandler:

    def __init__(self, sdk):
        self.sdk = sdk

        self.commands = {
            'add_counter': InlineAddCounter(self.sdk),
            'subscribe': CommandSubscribe(self.sdk).subscribe
        }

    async def __call__(self, payload):
        self.sdk.log("Inline commands handler fired with payload {}".format(payload))

        try:
            command, inline_params = payload['data'].split('|')
            payload['inline_params'] = inline_params
            if command in self.commands:
                await self.commands[command](payload)

        except Exception as e:
            self.sdk.log("Error: {}".format(e))
