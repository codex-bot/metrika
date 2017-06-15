from commands.add_counter import CommandAddCounter
from commands.delete_counter import CommandDeleteCounter
from commands.subscribe import CommandSubscribe
from commands.unsubscribe import CommandUnsubscribe
from commands.start import CommandStart
from commands.help import CommandHelp
from commands.counters import CommandCounters
from commands.access import CommandAccess


class InlineCommandsHandler:

    def __init__(self, sdk):
        self.sdk = sdk

        self.commands = {
            'add_counter': CommandAddCounter(self.sdk),
            'delete_counter': CommandDeleteCounter(self.sdk),
            'subscribe': CommandSubscribe(self.sdk).subscribe,
            'unsubscribe': CommandUnsubscribe(self.sdk),
            'start': CommandStart(self.sdk),
            'help': CommandHelp(self.sdk),
            'counters': CommandCounters(self.sdk),
            'access': CommandAccess(self.sdk),
        }

    async def __call__(self, payload):
        self.sdk.log("Inline commands handler fired with payload {}".format(payload))

        try:
            command_data = payload['data'].split('|')

            command = command_data[0]
            inline_params = None
            if len(command_data) > 1:
                inline_params = command_data[1]

            payload['inline_params'] = inline_params
            if command in self.commands:
                await self.commands[command](payload)

        except Exception as e:
            self.sdk.log("Error: {}".format(e))
