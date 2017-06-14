from commands.statistics import CommandStatistics
from .base import CommandBase


class CommandSubscribe(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/metrika_subscribe handler fired with payload {}".format(payload))

        if self.sdk.scheduler.find(payload['chat']):
            await self.sdk.send_text_to_chat(
                payload["chat"],
                "Вы уже подписаны на ежедневный дайджест в 19:00"
            )
        else:
            payload['command'] = 'today'
            self.sdk.scheduler.add(
                CommandStatistics(self.sdk).stats,
                chat_id=str(payload['chat']),
                hour='20',
                minute='12',
                args=[payload]
            )
            await self.sdk.send_text_to_chat(
                payload["chat"],
                "Вы успешно подписались на ежедневный дайджест в 19:00"
            )
