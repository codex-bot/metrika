from sdk.codexbot_sdk import CodexBot
from config import APPLICATION_TOKEN, APPLICATION_NAME, DB, SERVER, USERS_COLLECTION_NAME
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

        if 'code' not in request['query']:
            self.sdk.log("Metrika route handler: code is missed")
            return {
                'status': 404
            }

        if 'state' not in request['query']:
            self.sdk.log("Metrika route handler: user_token in state is missed")
            return {
                'status': 404
            }

        user_token = request['query']['state']

        # Get user data from DB by user token
        registered_chat = self.sdk.db.find_one(USERS_COLLECTION_NAME, {'user': user_token})

        # Check if chat was registered
        if not registered_chat or 'chat' not in registered_chat:
            self.sdk.log("Metrika route handler: wrong user token passed")
            return {
                'status': 404
            }

        #
        # TODO get access_token and save it
        #

        # Send notification
        message = "Авторизация прошла успешно."

        await self.sdk.send_to_chat(
            registered_chat['chat'],
            message
        )

        return {
            'text': 'OK!'
        }


if __name__ == "__main__":
    metrika = Metrika()
