from commands.statistics import CommandStatistics
from .base import CommandBase


class CommandSubscribe(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/metrika_subscribe handler fired with payload {}".format(payload))

        buttons = []
        time = 19

        for i in range(0,3):
            row = []

            for j in range(0,2):
                row.append({
                    'text': '{}:00'.format(str(time % 24).zfill(2)),
                    'callback_data': 'subscribe|{}'.format(time % 24)
                })
                time += 1

            buttons.append(row)

        await self.sdk.send_inline_keyboard_to_chat(payload['chat'], 'Выберете время', buttons)

    async def subscribe(self, payload):

        time = payload['inline_params']

        result = self.sdk.scheduler.find(payload['chat'])
        if result and result['hour'] == time:
            await self.sdk.send_text_to_chat(
                payload["chat"],
                "Вы уже подписаны на ежедневный дайджест в {}:00".format(time)
            )
        else:
            payload['command'] = 'today'
            self.sdk.scheduler.remove(payload['chat'])
            self.sdk.scheduler.add(
                CommandStatistics(self.sdk).stats,
                chat_id=str(payload['chat']),
                hour=time,
                args=[payload]
            )
            await self.sdk.send_text_to_chat(
                payload["chat"],
                "Вы успешно подписались на ежедневный дайджест в {}:00".format(time)
            )
