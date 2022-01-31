from urllib.parse import urlencode

import requests

from settings import METRIKA_OAUTH_APP_ID, METRIKA_OAUTH_APP_SECRET


class MetrikaAPI:

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

            button_rows = []
            for counter in result_json['counters']:
                button_rows.append([{
                    'text': "{} ({})".format(counter['name'], counter['site']),
                    'callback_data': "{}|{}".format('add_counter', str(counter['id']))
                }])
                counters.append(counter)

        except Exception as e:
            print("There was an error: %r" % e)
            return []

        return button_rows

    @staticmethod
    def get_counter_name(id, access_token):
        """
        Return counter name by id.
        Documentation: https://tech.yandex.ru/metrika/doc/api2/management/counters/counter-docpage/
        :param id: counter id
        :param access_token: access token
        :return: counter_name (JSON)
        """
        url = 'https://api-metrika.yandex.ru/management/v1/counter/{}?oauth_token={}'.format(id, access_token)
        # TODO: change requests to aiohttp
        r = requests.get(url=url)
        json = r.json()
        return "{} ({})".format(json['counter']['name'], json['counter']['site'])

    @staticmethod
    def get_user(token):
        params = {'oauth_token': token}

        try:
            result_json = requests.get('https://login.yandex.ru/info',
                                       params=params,
                                       headers={'Accept': 'application/x-yametrika+json'},
                                       timeout=5).json()

        except Exception as e:
            print("There was an error: %r" % e)
            return ''

        return result_json
