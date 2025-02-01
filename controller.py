import os
import sys
import time

from dotenv import load_dotenv

import auth
import lotto645
import notification
import win720


def buy_lotto645(authCtrl: auth.AuthController, cnt: int, mode: str):
    lotto = lotto645.Lotto645()
    _mode = lotto645.Lotto645Mode[mode.upper()]
    response = lotto.buy_lotto645(authCtrl, cnt, _mode)
    response["balance"] = lotto.get_balance(auth_ctrl=authCtrl)
    return response


def check_winning_lotto645(authCtrl: auth.AuthController) -> dict:
    lotto = lotto645.Lotto645()
    item = lotto.check_winning(authCtrl)
    return item


def buy_win720(authCtrl: auth.AuthController, username, jo: str, count: int):
    pension = win720.Win720()
    response = pension.buy_Win720(authCtrl, username, jo=jo, count=count)
    response["balance"] = pension.get_balance(auth_ctrl=authCtrl)
    return response


def check_winning_win720(authCtrl: auth.AuthController) -> dict:
    pension = win720.Win720()
    item = pension.check_winning(authCtrl)
    return item


def send_message(mode: int, lottery_type: int, response: dict, token, chat_ids):
    notify = notification.Notification()

    if mode == 0:
        if lottery_type == 0:
            notify.telegram_send_lotto_winning_message(response, token, chat_ids)
        else:
            notify.telegram_send_win720_winning_message(response, token, chat_ids)
    elif mode == 1:
        if lottery_type == 0:
            notify.telegram_send_lotto_buying_message(response, token, chat_ids)
        else:
            notify.telegram_send_win720_buying_message(response, token, chat_ids)


def check():
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    globalAuthCtrl = auth.AuthController()
    globalAuthCtrl.login(username, password)

    response = check_winning_lotto645(globalAuthCtrl)
    send_message(
        0, 0, response=response, token=telegram_token, chat_ids=[telegram_chat_id]
    )

    response = check_winning_win720(globalAuthCtrl)
    send_message(
        0, 1, response=response, token=telegram_token, chat_ids=[telegram_chat_id]
    )


def buy():
    load_dotenv()

    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    count = int(os.environ.get("COUNT"))
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    assert len(username) > 0
    assert len(password) > 0
    assert count > 0
    assert len(telegram_chat_id) > 0
    assert len(telegram_token) > 0

    mode = "AUTO"
    jo = "3"

    globalAuthCtrl = auth.AuthController()
    globalAuthCtrl.login(username, password)

    # response = buy_lotto645(globalAuthCtrl, count, mode)
    # send_message(
    #     1, 0, response=response, token=telegram_token, chat_ids=[telegram_chat_id]
    # )
    time.sleep(5)

    response = buy_win720(globalAuthCtrl, username=username, jo=jo, count=count)
    send_message(
        1, 1, response=response, token=telegram_token, chat_ids=[telegram_chat_id]
    )


def run():
    if len(sys.argv) < 2:
        print("Usage: python controller.py [buy|check]")
        return

    if sys.argv[1] == "buy":
        buy()
    elif sys.argv[1] == "check":
        check()


if __name__ == "__main__":
    run()
