import logging
from imap_tools import MailBox

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class ServerName:
    def __init__(self, email):
        if len(email.split('@')) > 1:
            if email.split('@')[1] in ('mail.ru', 'internet.ru', 'list.ru', 'bk.ru', 'inbox.ru', 'mail.ua', 'xmail.ru'):
                self.server = 'imap.mail.ru'
            elif email.split('@')[1] in ('yandex.ru', 'yandex.ua', 'narod.ru', 'ya.ru', 'yandex.com'):
                self.server = 'imap.yandex.ru'
            elif email.split('@')[1] in ('outlook.com', '1cbit.ru'):
                self.server = 'outlook.office365.com'
            else:
                logger.exception("Домен не из списка")
                raise ValueError("В настоящее время доступно только использование почтовых серверов Mail, Yandex "
                                 "и Outlook. Почтовый сервер Gmail не поддерживает IMAP, его использование"
                                 "невозможно. Для рассмотрения возможности использования вашего почтового "
                                 "сервера обратитесь к администратору бота @true_kapitan")
        else:
            logger.exception("Неверный формат электронной почты.")
            raise ValueError("Неверный формат электронной почты. Подключение невозможно")


class Mail(ServerName):
    def __init__(self, email: str, password: str):
        super().__init__(email)
        self.email = email
        self.password = password

    async def is_connect(self):
        try:
            with MailBox(self.server).login(username=self.email, password=self.password):
                return True
        except:
            return False

