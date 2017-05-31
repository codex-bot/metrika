import random
import string
from time import time

from sdk.codexbot_sdk import CodexBot
from config import APPLICATION_TOKEN, APPLICATION_NAME, DB, URL, SERVER


class Metrika:

    def __init__(self):

        self.sdk = CodexBot(APPLICATION_NAME, SERVER['host'], SERVER['port'], db_config=DB, token=APPLICATION_TOKEN)

        self.sdk.log("Metrika module initialized")

        self.sdk.register_commands([
            ('metrika_help', 'help', self.help),
            ('metrika_start', 'start', self.start)
        ])

        self.sdk.set_routes([
            # ('POST', '/metrika/{user_token}', self.metrika_route_handler)
        ])

        self.sdk.start_server()

    #
    #
    # HELP
    # todo: move to the class
    #

    async def help(self, payload):
        self.sdk.log("/help handler fired with payload {}".format(payload))

        message = "Модуль для работы с сервисом Яндекс.Метрика.\n\n" \
                  "Чтобы начать, выполните команду /metrika_start."

        await self.sdk.send_to_chat(
            payload["chat"],
            message
        )

    async def start(self, payload):
        self.sdk.log("/start handler fired with payload {}".format(payload))

        message = "Стартуем."

        await self.sdk.send_to_chat(
            payload["chat"],
            message
        )

if __name__ == "__main__":
    metrika = Metrika()
