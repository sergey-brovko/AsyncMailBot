import logging
import time
from bs4 import BeautifulSoup
from imap_tools import MailBox, A, OR, AND
import imaplib

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


class ActionByRules:

    def __init__(self, messages: list, action: str):
        self.messages = messages
        self.action = action

    def get_file(self) -> dict[str, list[tuple]] | None:
        for msg in self.messages:
            if msg:
                return {'files': [(att.filename, att.payload) for att in msg.attachments], 'from': msg.from_}

    def get_text(self) -> dict[str, str] | None:
        for msg in self.messages:
            if msg:
                soup = BeautifulSoup(msg.html, 'html.parser')
                text = list(soup.get_text(separator='\n'))
                text = [ch for i, ch in enumerate(text) if (ch != '\n') or (text[i - 1] != '\n')]
                text = [ch for i, ch in enumerate(text) if (ch != ' ') or (text[i - 1] != ' ')]
                return {'text': ''.join(text), 'from': msg.from_}

    def get_html(self) -> dict | None:
        for msg in self.messages:
            if msg:
                return {'html': msg.html, 'mail_id': msg.date_str, 'from': msg.from_}

    def get_msg_by_action(self) -> dict[str, dict[str, list[tuple]] | dict[str, str] | dict | None]:
        if self.action == 'all':
            return {'type': 'all', 'data': self.get_html()}
        elif self.action == 'file':
            return {'type': 'file', 'data': self.get_file()}
        elif self.action == 'text':
            return {'type': 'text', 'data': self.get_text()}


class MailFilter(Mail):
    def __init__(self, email: str, password: str, rules: list):
        super().__init__(email, password)
        self.rules = rules

    def get_response(self) -> list[dict[str, list[tuple] | str | dict | None]] | None:
        try:
            mailbox = MailBox(self.server)
        except Exception as e:
            logger.exception(f'## Ошибка в подключении к {self.server}, переподключение через минуту...', exc_info=e)
            time.sleep(60)
        else:
            try:
                mailbox.login(username=self.email, password=self.password)
                result = []
                for rule in self.rules:
                    messages = list(mailbox.fetch(AND(A(new=True), A(from_=rule[0].lower()))))
                    if messages:
                        msg = ActionByRules(messages=messages, action=rule[1]).get_msg_by_action()
                        logger.info(f"\nmessages:{messages}\n")
                        if msg.get('data'):
                            result.append(msg)
                mailbox.logout()
                return result
            except Exception as e:
                logger.exception(f'## Ошибка в получении письма для {self.email}', exc_info=e)
