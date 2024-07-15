from multiprocessing import Process
from mailboxes.catch_email import mail_worker
from bot_app.app import bot_run

if __name__ == '__main__':
    process_mail = Process(target=mail_worker)
    process_mail.start()
    bot_run()
    process_mail.join()

