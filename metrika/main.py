from sdk.codexbot_sdk import CodexBot
from config import APPLICATION_TOKEN, APPLICATION_NAME, DB, SERVER, USERS_COLLECTION_NAME
from commands.help import CommandHelp
from commands.start import CommandStart

import requests
from config import METRIKA_OAUTH_APP_ID, METRIKA_OAUTH_APP_SECRET

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
        code = request['query']['code']

        # Get user data from DB by user token
        registered_chat = self.sdk.db.find_one(USERS_COLLECTION_NAME, {'user': user_token})

        # Check if chat was registered
        if not registered_chat or 'chat' not in registered_chat:
            self.sdk.log("Metrika route handler: wrong user token passed")
            return {
                'status': 404
            }

        ## <getting access_token> ##
        # TODO move this to function
        url = 'https://oauth.yandex.ru/token'
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': METRIKA_OAUTH_APP_ID,
            'client_secret': METRIKA_OAUTH_APP_SECRET
        }
        headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        r = requests.post(
            url = url,
            data = data,
            headers = headers
        )
        response = r.json()

        """
        In 'response' or 'r.json()' u can find:
        {
            "token_type": "bearer",
            "access_token": "AQAAAAACHQerAAR12345678abcd",
            "expires_in": 31535975,
            "refresh_token": "1:DOgz_PampAMPAM:UNder-MYSpac3:vatIsIT-gdeK0d"
        }
        """

        # Is access_token exist
        if not response or 'access_token' not in response:
            self.sdk.log("Metrika route handler: no access_token in response")
            return {
                'status': 404
            }
        ## </getting access_token> ##

        ## <saving access_token> ##
        # TODO save this token_type
        ## </saving access_token> ##

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
