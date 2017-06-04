from sdk.codexbot_sdk import CodexBot
from config import APPLICATION_TOKEN, APPLICATION_NAME, DB, SERVER
from commands.help import CommandHelp
from commands.start import CommandStart

class Metrika:

    def __init__(self):

        self.sdk = CodexBot(APPLICATION_NAME, SERVER['host'], SERVER['port'], db_config=DB, token=APPLICATION_TOKEN)

        self.sdk.log("Metrika module initialized")

        self.sdk.register_commands([
            ('metrika_help', 'help', CommandHelp(self.sdk)),
            ('metrika_start', 'start', CommandStart(self.sdk))
        ])

        self.sdk.set_routes([
            ('GET', '/metrika/callback', self.metrika_route_handler)
        ])

        self.sdk.start_server()

    @CodexBot.http_response
    async def metrika_route_handler(self, request):
        # self.sdk.log("Callback from yandex.metrika auth with request {}".format(request))

        print(request['query'])

        message = "Авторизация прошла успешно."

        self.sdk.log(message)

        # await self.sdk.send_to_chat(
        #     # payload["chat"],
        #     '2JMAGGW9',
        #     message
        # )

        return {
            'text': 'OK!'
        }


if __name__ == "__main__":
    metrika = Metrika()
