from mailboxes.database.models import async_session
from sqlalchemy import select
from mailboxes.database.models import User, Mailbox, Rule
from mailboxes.encryption.crypt import decrypt


async def get_all_rules() -> list[tuple[dict, list[tuple[any, any]]]] | None:
    async with async_session() as session:
        result = []
        mailboxes = await session.execute(select(Mailbox.email, Mailbox.password, Mailbox.mailbox_id, User.chat_id)
                                          .join(User, Mailbox.user_id == User.user_id)
                                          .where(User.receive_letters == True))
        for mailbox in mailboxes:
            rules = await session.execute(select(Rule.email, Rule.action)
                                          .where(Rule.mailbox_id == mailbox[2]))
            result.append(({'email': mailbox[0], 'password': decrypt(mailbox[1]), 'chat_id': mailbox[3]}, rules))

        return result
