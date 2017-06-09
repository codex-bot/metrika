from .base import CommandBase


class CommandHelp(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/help handler fired with payload {}".format(payload))

        message = "Модуль для работы с сервисом Яндекс.Метрика.\n\n" \
                  "Чтобы начать, выполните команду /metrika_start."

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )
