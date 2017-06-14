from commands.subscribe import CommandSubscribe
from commands.statistics import CommandStatistics
from commands.unsubscribe import CommandUnsubscribe
from events.auth import EventAuth
from inline import InlineCommandsHandler
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
            ('metrika_subscribe', 'metrika_subscribe', CommandSubscribe(self.sdk)),
            ('metrika_unsubscribe', 'metrika_unsubscribe', CommandUnsubscribe(self.sdk)),
            ('today', 'today', CommandStatistics(self.sdk).stats),
            ('weekly', 'weekly', CommandStatistics(self.sdk).stats),
            ('monthly', 'monthly', CommandStatistics(self.sdk).stats)
        ])

        self.sdk.set_routes([
            ('GET', '/metrika/callback', self.route_handler)
        ])

        self.sdk.set_callback_query_handler(InlineCommandsHandler(self.sdk))

        self.sdk.scheduler.restore(self.processor)

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

    def processor(self, params):
        return CommandStatistics(self.sdk).stats

if __name__ == "__main__":
    metrika = Metrika()
