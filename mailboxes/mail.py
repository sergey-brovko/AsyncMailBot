from imap_tools import MailBox, A
from bs4 import BeautifulSoup


class ServerName:
    def __init__(self, email):
        if len(email.split('@')) > 1:
            if email.split('@')[1] in ('mail.ru', 'internet.ru', 'list.ru', 'bk.ru', 'inbox.ru', 'mail.ua', 'xmail.ru'):
                self.server = 'imap.mail.ru'
            elif email.split('@')[1] in ('yandex.ru', 'yandex.ua', 'narod.ru', 'ya.ru', 'yandex.com'):
                self.server = 'imap.yandex.ru'
            else:
                raise ValueError("В настоящее время доступно только использование почтовых серверов Mail и Yandex. Для "
                                 "рассмотрения возможности использования вашего почтового сервера обратитесь к "
                                 "администратору бота @true_kapitan")
        else:
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


class MailFilter(Mail):
    def __init__(self, email: str, password: str, from_email: str):
        super().__init__(email, password)
        self.from_email = from_email


class MailFile(MailFilter):
    async def get_response(self):
        with MailBox(self.server).login(username=self.email, password=self.password) as mailbox:
            for msg in mailbox.fetch(criteria=A('NEW', f'FROM "{self.from_email}"'), reverse=True):
                if msg:
                    return [(att.filename, att.payload) for att in msg.attachments]


class MailText(MailFilter):
    async def get_response(self):
        with MailBox(self.server).login(username=self.email, password=self.password) as mailbox:
            for msg in mailbox.fetch(criteria=A('NEW', f'FROM "{self.from_email}"'), reverse=True):
                if msg:
                    soup = BeautifulSoup(msg.html, 'html.parser')
                    return soup.get_text(separator='\n') + self.from_email
