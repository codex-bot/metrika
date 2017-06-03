from .base import CommandBase


class CommandHelp(CommandBase):

    async def help(self, payload):
        self.sdk.log("/help handler fired with payload {}".format(payload))

        message = "Модуль для работы с сервисом Яндекс.Метрика.\n\n" \
                  "Чтобы начать, выполните команду /metrika_start."

        await self.sdk.send_to_chat(
            payload["chat"],
            message
        )
