from multiprocessing import Process
from mailboxes.catch_email import mail_worker
from bot_app.app import bot_run
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler2 = logging.FileHandler(f"{__name__}.log", mode='w')
formatter2 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler2.setFormatter(formatter2)
logger.addHandler(handler2)
logger.info(f"Testing the custom logger for module {__name__}...")


if __name__ == '__main__':
    try:
        process_mail = Process(target=mail_worker)
        process_mail.start()
        bot_run()
        logger.info("Бот успешно запущен")
        process_mail.join()
        logger.info("Работа бота остановлена")
    except Exception as e:
        logger.exception("Exception")
