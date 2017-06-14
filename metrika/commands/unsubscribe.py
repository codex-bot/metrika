from sched import scheduler

from .base import CommandBase


class CommandUnsubscribe(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/metrika_unsubscribe handler fired with payload {}".format(payload))

        if self.sdk.scheduler.find(payload['chat']):
            try:
                self.sdk.scheduler.remove(payload['chat'])
                # if self.sdk.scheduler.get_job(str(payload['chat'])):
                #     self.sdk.scheduler.remove_job(str(payload['chat']))

                await self.sdk.send_text_to_chat(
                    payload["chat"],
                    "Вы успешно отписались от ежедневного дайджеста"
                )
            except Exception as e:
                self.sdk.log("Error: {}".format(e))
        else:
            await self.sdk.send_text_to_chat(
                payload["chat"],
                "Вы не подписаны на ежедневный дайджест"
            )
