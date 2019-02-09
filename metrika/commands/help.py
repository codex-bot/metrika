from .base import CommandBase


class CommandHelp(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/help handler fired with payload {}".format(payload))

        message = "Этот модуль поможет вам следить за статистикой сайта.\n" \
                  "Возможности модуля:\n\n" \
                  "- моментальное получение текущих значений счетчиков (DAU, просмотры, источники) за период (день, неделя, месяц)\n" \
                  "- уведомление о достижении целей (например, бот сообщит о достижении показателя в 10k уникальных посетителей)\n\n" \
                  "/metrika - перечень команд\n" \
                  "/metrika_add - добавление нового пользователя Яндекс.Метрика\n" \
                  "/metrika_subscriptions - настройка ежедневных отчётов\n" \
                  "/metrika_stop - отключение счетчиков\n" \
                  "/metrika_counters - список подключенных счётчиков\n" \
                  "/metrika_access - отключение пользователей от чата\n" \
                  "/today, /weekly, /monthly - получить статистику посещений за сегодняшний день/неделю/месяц"

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )
