from .base import CommandBase


class CommandStatistics(CommandBase):
    """
    Return statistics for /today, /weekly, /monthly
    """

    async def today(self, payload):

        chat_records = list(self.sdk.db.find('metrika_tokens', {'chat_id': payload["chat"]}))

        if not len(chat_records):
            return await self.sdk.send_to_chat(
                payload["chat"],
                "Не авторизован ни один пользователь\n" \
                "\n" \
                "Для авторизации используйте /metrika_add"
            )

        message = "Данные за сегодняшний день\n\n"

        await self.sdk.send_to_chat(
            payload["chat"],
            message
        )
