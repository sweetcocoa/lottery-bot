import telegram
import asyncio
import sys

TELEGRAM_MAX_MESSAGE_LENGTH = 4096


class Notification:
    async def asend_telegram_message(self, token, chat_ids, message):
        messages = [
            message[i : i + TELEGRAM_MAX_MESSAGE_LENGTH]
            for i in range(0, len(message), TELEGRAM_MAX_MESSAGE_LENGTH)
        ]

        if len(messages) > 2:
            messages = [
                messages[0],
                "\n\n ... \n\n [skipped by sweetdebug] \n\n ... \n\n",
                (messages[-2] + messages[-1])[-TELEGRAM_MAX_MESSAGE_LENGTH:],
            ]

        try:
            async with telegram.Bot(token) as bot:
                for chat_id in chat_ids:
                    for message in messages:
                        await bot.send_message(chat_id=str(chat_id), text=message)
        except telegram.error.TelegramError as e:
            print(f"sweetdebug : telegram error, {e}, {type(e)}", file=sys.stderr)

    def send_telegram_message(self, token, chat_ids, message):
        return asyncio.run(
            self.asend_telegram_message(token, chat_ids=chat_ids, message=message)
        )

    def telegram_send_lotto_buying_message(self, body: dict, token, chat_ids):
        assert isinstance(token, str)
        assert isinstance(chat_ids, (list, tuple))
        assert isinstance(chat_ids[0], str)

        result = body.get("result", {})
        if result.get("resultMsg", "FAILURE").upper() != "SUCCESS":
            return

        lotto_number_str = self.make_lotto_number_message(result["arrGameChoiceNum"])
        message = f"{result['buyRound']}회 로또 구매 완료 :moneybag: 남은잔액 : {body['balance']}\n```{lotto_number_str}```"
        self.send_telegram_message(token, chat_ids, message)

    def make_lotto_number_message(self, lotto_number: list) -> str:
        assert type(lotto_number) == list

        # parse list without last number 3
        lotto_number = [x[:-1] for x in lotto_number]

        # remove alphabet and | replace white space  from lotto_number
        lotto_number = [x.replace("|", " ") for x in lotto_number]

        # lotto_number to string
        lotto_number = "\n".join(x for x in lotto_number)

        return lotto_number

    def telegram_send_win720_buying_message(self, body: dict, token, chat_ids):
        assert isinstance(token, str)
        assert isinstance(chat_ids, (list, tuple))
        assert isinstance(chat_ids[0], str)

        if body.get("resultCode") != "100":
            return

        win720_round = body.get("resultMsg").split("|")[3]

        win720_number_str = self.make_win720_number_message(body.get("saleTicket"))
        message = f"{win720_round}회 연금복권 구매 완료 :moneybag: 남은잔액 : {body['balance']}\n```{win720_number_str}```"
        self.send_telegram_message(token, chat_ids, message)

    def make_win720_number_message(self, win720_number: str) -> str:
        return "\n".join(win720_number.split(","))

    def telegram_send_lotto_winning_message(self, winning: dict, token, chat_ids):
        assert type(winning) == dict
        assert isinstance(token, str)
        assert isinstance(chat_ids, (list, tuple))
        assert isinstance(chat_ids[0], str)

        message = f"""{winning['kind']} {winning['round']}회 결과
구매날짜 : {winning['purchased_date']}
추첨날짜 : {winning['winning_date']}
결과 : {winning['status']}
금액 : {winning['money']}
매수 : {winning['count']}
        """

        self.send_telegram_message(token, chat_ids, message)

    def telegram_send_win720_winning_message(self, winning: dict, token, chat_ids):
        assert type(winning) == dict
        assert isinstance(token, str)
        assert isinstance(chat_ids, (list, tuple))
        assert isinstance(chat_ids[0], str)

        message = f"""{winning['kind']} {winning['round']}회 결과
구매날짜 : {winning['purchased_date']}
추첨날짜 : {winning['winning_date']}
결과 : {winning['status']}
금액 : {winning['money']}
매수 : {winning['count']}
        """

        self.send_telegram_message(token, chat_ids, message)
