from commands.statistics import CommandStatistics
from .base import CommandBase


class CommandSubscribe(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/metrika_subscribe handler fired with payload {}".format(payload))

        schedule = self.sdk.db.find_one("metrika_schedules", {'chat_id': payload['chat']})

        if schedule:
            await self.sdk.send_text_to_chat(
                payload["chat"],
                "Вы уже подписаны на ежедневный дайджест в 19:00"
            )
        else:
            self.sdk.db.insert("metrika_schedules", {'chat_id': payload['chat']})
            payload['command'] = 'today'
            if not self.sdk.scheduler.get_job(str(payload['chat'])):
                self.sdk.scheduler.add_job(
                    CommandStatistics(self.sdk).stats,
                    args=[payload],
                    trigger='cron',
                    hour='19',
                    id=str(payload['chat']),
                    replace_existing=True)
            await self.sdk.send_text_to_chat(
                payload["chat"],
                "Вы успешно подписались на ежедневный дайджест в 19:00"
            )
