from commands.statistics import CommandStatistics
from events.auth import EventAuth
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
            ('metrika_start', 'start', CommandStart(self.sdk)),
            ('today', 'today', CommandStatistics(self.sdk).today)
        ])

        self.sdk.set_routes([
            ('GET', '/metrika/callback', self.route_handler)
        ])

        self.sdk.start_server()

    @CodexBot.http_response
    async def route_handler(self, request):
        """
        Process callback from Yandex Metrika after oauth authentication.
        :param request:
        :return:
        """

        result = await EventAuth(self.sdk)(request)

        if result:
            return {'text': 'OK'}
        else:
            return {'status': 404}


if __name__ == "__main__":
    metrika = Metrika()
