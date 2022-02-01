from .statistics import CommandStatistics
from .base import CommandBase


class CommandSubscribe(CommandBase):
    """
    /metrika_subscribe command processor
    Ask for time 18:00, 19:00, 20:00, 21:00, 22:00, 23:00 or 00:00
    """

    async def __call__(self, payload):
        """
        Ask for appropriate time and send keyboard with options.
        :param payload:
        :return:
        """
        self.sdk.log("/metrika_subscribe handler fired with payload {}".format(payload))

        buttons = []
        time = 19

        for rows in range(0,3):
            row = []

            for cols in range(0,2):
                row.append({
                    'text': '{}:00'.format(str(time % 24).zfill(2)),
                    'callback_data': 'subscribe|{}'.format(time % 24)
                })
                time += 1

            buttons.append(row)

        buttons.append([
            {
                'text': 'Отписаться',
                'callback_data': 'unsubscribe'
            }
        ])

        await self.sdk.send_inline_keyboard_to_chat(payload['chat'], 'Выберете время', buttons)

    async def subscribe(self, payload):
        """
        Inline command for setting new scheduling time
        :param payload:
            - chat - chat ID
            - inline_params - time in format HH:mm
            - command - command for callback ('today', 'weekly', 'monthly')
        """

        time = payload['inline_params']

        if not time:
            await self.__call__(payload)
            return

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
