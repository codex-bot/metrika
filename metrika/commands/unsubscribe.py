from sched import scheduler

from .base import CommandBase


class CommandUnsubscribe(CommandBase):
    """
        /metrika_unsubscribe command processor.
    """

    async def __call__(self, payload):
        """
        - Try to find scheduler job for the chat with chat_id.
        - If chat is found - remove job and delete from DB.
        :param payload:
            - chat_id - chat ID
        """
        self.sdk.log("/metrika_unsubscribe handler fired with payload {}".format(payload))

        if self.sdk.scheduler.find(payload['chat']):
            try:
                self.sdk.scheduler.remove(payload['chat'])

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
