import requests
from .base import CommandBase


class InlineAddCounter(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("Inline keyboard handler fired with payload {}".format(payload))

        try:
            inline_params = payload['inline_params']
            chat_id = payload['chat']
            user_id = payload['user']

            counter_id = inline_params
            access_token = self.get_access_token(user_id)
            if not access_token:
                return await self.sdk.send_text_to_chat(
                    payload["chat"],
                    "Ошибка получения токена доступа"
                )

            counter_name = self.get_counter_name(counter_id, access_token)
            if not counter_name:
                return await self.sdk.send_text_to_chat(
                    payload["chat"],
                    "Ошибка получения имени счётчика"
                )

            if self.sdk.db.find_one('metrika_counters', {'chat_id': chat_id, 'counter_id': counter_id}):
                await self.sdk.send_text_to_chat(
                    payload["chat"],
                    'Счетчик *{}* уже прикреплен к данному чату.'.format(counter_name),
                    'Markdown'
                )
            else:
                self.sdk.db.insert('metrika_counters', {
                    'chat_id': chat_id,
                    'counter_id': counter_id,
                    'user_id': user_id,
                    'counter_name': counter_name
                })
                await self.sdk.send_text_to_chat(
                    payload["chat"],
                    'Готово! Счетчик *{}* успешно прикреплен к данному чату.'.format(counter_name),
                    'Markdown'
                    )
        except Exception as e:
            self.sdk.log("Error: {}".format(e))

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
        return r.json()['counter']['name']

    def get_access_token(self, user_id):
        try:
            return self.sdk.db.find_one('metrika_tokens', {'user_id': user_id})['access_token']
        except:
            return None
