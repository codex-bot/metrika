from .base import CommandBase
from api import MetrikaAPI


class CommandAddCounter(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("Add counter handler fired with payload {}".format(payload))

        try:
            inline_params = payload.get('inline_params', None)
            chat_id = payload['chat']
            user_id = payload['user']

            if not inline_params:
                await self.list(payload)
                return

            counter_id = inline_params
            access_token = self.get_access_token(user_id)
            if not access_token:
                return await self.sdk.send_text_to_chat(
                    payload["chat"],
                    "Ошибка получения токена доступа"
                )

            counter_name = MetrikaAPI.get_counter_name(counter_id, access_token)
            if not counter_name:
                return await self.sdk.send_text_to_chat(
                    payload["chat"],
                    "Ошибка получения имени счётчика"
                )

            if self.sdk.db.find_one(self.COLLECTIONS['counters'], {'chat_id': chat_id, 'counter_id': counter_id}):
                await self.sdk.send_text_to_chat(
                    payload["chat"],
                    'Счетчик *{}* уже прикреплен к данному чату.'.format(counter_name),
                    'Markdown'
                )
            else:
                user = self.sdk.db.find_one(self.COLLECTIONS['tokens'], {'access_token': access_token})

                self.sdk.db.insert(self.COLLECTIONS['counters'], {
                    'chat_id': chat_id,
                    'counter_id': counter_id,
                    'user_id': user_id,
                    'user_login': user['user_info']['login'],
                    'counter_name': counter_name
                })
                await self.sdk.send_text_to_chat(
                    payload["chat"],
                    'Готово! Счетчик *{}* успешно прикреплен к данному чату.'.format(counter_name),
                    'Markdown'
                    )
        except Exception as e:
            self.sdk.log("Error: {}".format(e))

    async def list(self, payload):

        token = self.get_access_token(payload['user'])

        if not token:
            await self.sdk.send_text_to_chat(payload['chat'], 'Не авторизован ни один пользователь')
            return

        counters = MetrikaAPI.get_counters(token)

        await self.sdk.send_inline_keyboard_to_chat(
            payload['chat'],
            "Выберите счетчик для подключения",
            counters
        )
