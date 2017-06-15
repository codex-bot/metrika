from commands.subscribe import CommandSubscribe
from commands.statistics import CommandStatistics
from commands.unsubscribe import CommandUnsubscribe
from events.auth import EventAuth
from inline import InlineCommandsHandler
from sdk.codexbot_sdk import CodexBot
from config import APPLICATION_TOKEN, APPLICATION_NAME, DB, SERVER
from commands.help import CommandHelp
from commands.start import CommandStart
from commands.metrika import CommandMetrika
from commands.delete_counter import CommandDeleteCounter
from commands.counters import CommandCounters
from commands.access import CommandAccess


class Metrika:

    def __init__(self):

        self.sdk = CodexBot(APPLICATION_NAME, SERVER['host'], SERVER['port'], db_config=DB, token=APPLICATION_TOKEN)

        self.sdk.log("Metrika module initialized")

        self.sdk.register_commands([
            ('metrika', 'Приложение для Яндекс.Метрики. Умеет присылать статистику посещений сайтов.', CommandMetrika(self.sdk)),
            ('metrika_help', 'Help', CommandHelp(self.sdk)),
            ('metrika_start', 'Start', CommandStart(self.sdk)),
            ('metrika_add', 'Add new metrika user', CommandStart(self.sdk)),
            ('metrika_subscriptions', 'Everyday statistics', CommandSubscribe(self.sdk)),
            ('metrika_unsubscribe', 'Unsubscribe', CommandUnsubscribe(self.sdk)),
            ('metrika_stop', 'Delete counter', CommandDeleteCounter(self.sdk)),
            ('metrika_counters', 'Available counters', CommandCounters(self.sdk)),
            ('metrika_access', 'Access settings', CommandAccess(self.sdk)),
            ('today', 'Today statistics', CommandStatistics(self.sdk).stats),
            ('weekly', 'Week statistics', CommandStatistics(self.sdk).stats),
            ('monthly', 'Month statistics', CommandStatistics(self.sdk).stats)
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
