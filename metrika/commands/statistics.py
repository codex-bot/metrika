from .base import CommandBase


class CommandStatistics(CommandBase):

    async def today(self, payload):

        chat_records = list(self.sdk.db.find('metrika_tokens', {'chat_id': payload["chat"]}))

        if not len(chat_records):
            return await self.sdk.send_to_chat(
                payload["chat"],
                "Не авторизован ни один пользователь\n" \
                "\n" \
                "Для авторизации используйте /metrika_add"
            )

        message = "Данные за текущий месяц\n\n"

        for chat_record in chat_records:
            try:
                counters = list(self.sdk.db.find('metrika_counters', {
                    'chat_id': self.chat_id,
                    'login': chat_record['access_token']
                }))

                if not len(counters):
                    message = 'Не подключен ни один счетчик\n\nДля подключения доступных счетчиков используйте /metrika_available.'

                for counter in counters:
                    metrikaAPI = MetrikaAPI(token['access_token'], counter['counter_id'], self.chat_id)
                    result = metrikaAPI.get_visit_statistics(cmd)
                    if result:
                        print(result)
                        users, hits = result
                        message += "%s:\n%d уникальных посетителей\n%d просмотров\n\n" % (counter['counter_name'],
                                                                                          users, hits)

            except Exception as e:
                logging.warning("Metrika API exception: %s" % e)


        await self.sdk.send_to_chat(
            payload["chat"],
            message
        )

    def get_