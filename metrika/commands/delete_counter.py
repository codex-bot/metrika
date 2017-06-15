from .base import CommandBase


class CommandDeleteCounter(CommandBase):

    async def __call__(self, payload):

        try:
            inline_params = payload.get('inline_params', None)
            chat_id = payload['chat']
            user_id = payload['user']

            if not inline_params:
                await self.list(payload)
                return

            counter_id = inline_params

            counter = self.sdk.db.find_one(self.COLLECTIONS['counters'], {'chat_id': chat_id, 'counter_id': counter_id})

            self.sdk.db.remove(self.COLLECTIONS['counters'], {'chat_id': chat_id, 'counter_id': counter_id})

            await self.sdk.send_text_to_chat(
                payload["chat"],
                'Счетчик *{}* успешно отключен.'.format(counter['counter_name']),
                'Markdown'
            )

        except Exception as e:
            self.sdk.log("Error: {}".format(e))

    async def list(self, payload):

        chat_counters = self.get_chat_counters(payload['chat'])

        if not len(chat_counters):
            await self.sdk.send_text_to_chat(payload['chat'], 'Подключенных счетчиков не найдено')
            return

        counters = []

        for counter in chat_counters:
            counters.append([{
                'text': counter['counter_name'],
                'callback_data': '{}|{}'.format('delete_counter', counter['counter_id'])
            }])

        await self.sdk.send_inline_keyboard_to_chat(
            payload['chat'],
            "Выберите счетчик, который хотите отключить",
            counters
        )

    def get_access_token(self, user_id):
        try:
            return self.sdk.db.find_one('metrika_tokens', {'user_id': user_id})['access_token']
        except:
            return None
