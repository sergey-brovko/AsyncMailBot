from multiprocessing import Process
from mailboxes.catch_email import mail_worker
from bot_app.app import bot_run

if __name__ == '__main__':
    process_bot = Process(target=bot_run)
    process_mail = Process(target=mail_worker)
    process_bot.start()
    process_mail.start()
    process_mail.join()
    process_bot.join()

