import logging
from email.policy import default
from email import message_from_bytes
import quopri

logger = logging.getLogger("email")


class MongoSMTPHandler:
    def __init__(self, mongo, database_name):
        self.mongo = mongo
        self.db = mongo[database_name]

    def get_parsed_body(self, envelope):
        msg = message_from_bytes(envelope.content, policy=default)
        subject = msg.get("Subject")
        msg = msg.get_payload()
        if isinstance(msg, str):
            return subject, msg, None

        text_content = None
        html_content = None
        for payload in msg:
            content_type = payload.get_content_type()
            if "text" in content_type:
                d = quopri.decodestring(payload.get_payload())
                charset = payload.get_content_charset()
                if "html" in content_type:
                    html_content = d.decode(charset)

                else:
                    text_content = d.decode(charset)
        return subject, text_content, html_content

    async def handle_DATA(self, server, session, envelope):
        subject, text_content, html_content = self.get_parsed_body(envelope=envelope)
        document = {
            'from': envelope.mail_from,
            'to': envelope.rcpt_tos,
            'subject': subject,
            'raw_message': envelope.content,
            'text': text_content,
            'html': html_content
        }
        result = await self.db.received.insert_one(document)
        logger.info('New email to %s with id %s', envelope.rcpt_tos, repr(result.inserted_id))
        return '250 OK'
