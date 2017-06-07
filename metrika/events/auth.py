import requests
from urllib.parse import urlencode
from config import METRIKA_OAUTH_APP_ID, METRIKA_OAUTH_APP_SECRET
from events.base import EventBase


class EventAuth(EventBase):
    """
    Process OAuth Event. Obtain access token and save it to DB.
    1. Get code and state from request.
    2. Send code and get access token from Yandex.
    3. Insert pair (access_toke, chat_id) to DB 'metrika_tokens' if not exists
    4. Build buttons list with counters for the access token.
    5. Send success message
    """

    async def __call__(self, request):
        if 'code' not in request['query']:
            self.sdk.log("Metrika route handler: code is missed")
            return False

        if 'state' not in request['query']:
            self.sdk.log("Metrika route handler: user_token in state is missed")
            return False

        chat_id = request['query']['state']
        code = request['query']['code']

        try:
            access_token_response = EventAuth.get_access_token(code)
            access_token = access_token_response['access_token']
        except Exception as e:
            self.sdk.log("Error: {}".format(e))
            return False
        else:
            if not self.sdk.db.find_one('metrika_tokens', {'access_token': access_token, 'chat_id': chat_id}):
                self.sdk.db.insert('metrika_tokens', {
                    'access_token': access_token,
                    'chat_id': chat_id
                })

            # Show available counters to the chat
            counters = EventAuth.get_counters(access_token)
            self.sdk.log(counters)
            # TODO: Show list of buttons
            await self.sdk.send_to_chat(
                chat_id,
                "Пользователь Яндекс.Метрика успешно добавлен."
            )

        return True

    @staticmethod
    def get_counters(access_token):
        """
        Return counters list for the specific access token.
        Documentation: https://tech.yandex.com/metrika/doc/api2/management/counters/counters-docpage/
        :param access_token: string
        :return: list(counters JSON)
        """
        params = urlencode({
            'id': METRIKA_OAUTH_APP_ID,
            'oauth_token': access_token
        })
        counters = []

        try:
            result_json = requests.get('https://api-metrika.yandex.ru/management/v1/counters',
                                       params=params,
                                       headers={'Accept': 'application/x-yametrika+json'},
                                       timeout=5
                                       ).json()

            for counter in result_json['counters']:
                counters.append(counter)

        except Exception as e:
            print("There was an error: %r" % e)
            return []

        return counters

    @staticmethod
    def get_access_token(code):
        """
        Return access token in exchange for code.
        Documentation: https://tech.yandex.ru/oauth/doc/dg/reference/auto-code-client-docpage/
        :param code: string
        :return: access_token (JSON)
        """
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
        # TODO: change requests to aiohttp
        r = requests.post(
            url=url,
            data=data,
            headers=headers
        )
        return r.json()
