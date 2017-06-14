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
                    'text': '{}:00'.format(time),
                    'callback_data': 'subscribe|{}'.format(time)
                })
                time += 1

            buttons.append(row)

        await self.sdk.send_inline_keyboard_to_chat(payload['chat'], 'Выберете время', buttons)

    async def subscribe(self, payload):

        time = payload['inline_params']

        if self.sdk.scheduler.find(payload['chat']):
            await self.sdk.send_text_to_chat(
                payload["chat"],
                "Вы уже подписаны на ежедневный дайджест в {}:00".format(time)
            )
        else:
            payload['command'] = 'today'
            if not self.sdk.scheduler.get_job(str(payload['chat'])):
                self.sdk.scheduler.add_job(
                    CommandStatistics(self.sdk).stats,
                    args=[payload],
                    trigger='cron',
                    hour=time,
                    id=str(payload['chat']),
                    replace_existing=True)
            await self.sdk.send_text_to_chat(
                payload["chat"],
                "Вы успешно подписались на ежедневный дайджест в {}:00".format(time)
            )
