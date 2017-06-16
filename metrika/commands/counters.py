from .base import CommandBase


class CommandCounters(CommandBase):

    async def __call__(self, payload):

        counters = self.get_chat_counters(payload['chat'])

        if not len(counters):
            await self.sdk.send_text_to_chat(payload['chat'], 'Подключенных счетчиков не найдено')
            return

        users = {}
        for counter in counters:
            login = counter.get('user_login')
            counter_name = counter.get('counter_name')
            if login in users:
                users[login].append(counter_name)
            else:
                users[login] = [counter_name]

        message = 'Подключенные счетчики:\n\n'
        for login in users.keys():
            message += '*@{}*\n'.format(login)
            for counter in users[login]:
                message += '{}\n'.format(counter)
            message += '\n'

        await self.sdk.send_text_to_chat(payload['chat'], message, parse_mode='Markdown')