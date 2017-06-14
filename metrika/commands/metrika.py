from .base import CommandBase


class CommandMetrika(CommandBase):

    async def __call__(self, payload):

        buttons = [
            ('Добавить пользователя', 'start'),
            ('Добавить счетчик', 'add_counter'),
            ('Регулярные отчеты', 'subscribe'),
            ('Удалить счетчик', 'delete_counter'),
            ('Подключенные счетчики', 'counters'),
            ('Управление доступом', 'access'),
            ('Помощь', 'help')
        ]

        keyboard = []

        for button in buttons:
            keyboard.append([{
                'text': button[0],
                'callback_data': button[1]
            }])

        await self.sdk.send_inline_keyboard_to_chat(payload['chat'], 'Действия:', keyboard)
