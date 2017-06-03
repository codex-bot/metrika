from .base import CommandBase


class CommandStart(CommandBase):

    async def start(self, payload):
        self.sdk.log("/start handler fired with payload {}".format(payload))

        message = "Стартуем."

        await self.sdk.send_to_chat(
            payload["chat"],
            message
        )
