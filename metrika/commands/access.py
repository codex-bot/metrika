from .base import CommandBase


class CommandAccess(CommandBase):

    async def __call__(self, payload):

        if payload.get('inline_params', None):
            await self.remove_user(payload)
            return

        users = list(self.sdk.db.find(self.COLLECTIONS['tokens'], {'chat_id': payload['chat']}))

        buttons = []

        for user in users:
            buttons.append([{
                'text': '@{}'.format(user['user_info']['login']),
                'callback_data': '{}|{}'.format('access', user['user_id'])
            }])

        await self.sdk.send_inline_keyboard_to_chat(
            payload["chat"],
            'Выберите пользователя, которого хотите отключить',
            buttons
        )

    async def remove_user(self, payload):
        user_id = payload['inline_params']

        user = self.sdk.db.find_one(self.COLLECTIONS['tokens'], {'user_id': user_id})

        if not user:
            await self.sdk.send_text_to_chat(payload['chat'],
                                             'Этот пользователь не подключен к чату')
            return

        self.sdk.db.remove(self.COLLECTIONS['tokens'], {'user_id': user_id})
        self.sdk.db.remove(self.COLLECTIONS['counters'], {'user_id': user_id})

        await self.sdk.send_text_to_chat(payload['chat'],
                                         "Пользователь *@{}* отключен".format(user['user_info']['login']),
                                         parse_mode='Markdown')
