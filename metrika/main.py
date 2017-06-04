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
            #('POST', '/metrika/callback', self.metrika_route_handler)
        ])

        self.sdk.start_server()


if __name__ == "__main__":
    metrika = Metrika()
