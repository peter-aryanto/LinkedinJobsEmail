MAX_LINKEDIN_JOBS_EMAILS = 4
MAX_LATEST_EMAILS = 20


from dotenv import load_dotenv
import base64
import os
from imapclient import IMAPClient
from email.header import decode_header, make_header  # This is built-in, NO need for `pip install`.
import email  # This is built-in, NO need for `pip install`.
from typing import List

load_dotenv()

YMAIL = os.getenv("YMAIL")
YAPP_PASSWORD = os.getenv("YAPP_PASSWORD") or "matamu" # https://login.yahoo.com/account/security?.lang=en-US&.intl=us&.src=yhelp → https://login.yahoo.com/myaccount/security/?.lang=en-US&.intl=us&.src=yhelp&.scrumb=qCwrl830s2G&anchorId=appPasswordCard

BREAK_CHAR_COUNT = 12


def readLinkedinJobsEmail() -> List[str]:
    jobs = []

    try:
        with IMAPClient("imap.mail.yahoo.com", ssl=True) as mail:
            mail.login(YMAIL, YAPP_PASSWORD)

            mail.select_folder("INBOX")
            messages = mail.search(["UNSEEN"])
            messages = sorted(messages, reverse=True)
            print(f"Unread Emails: {len(messages)}")

            if not messages:
                raise Exception ("Cannot find any unread email!")

            linkedinJobsEmailCounter = 0

            for msg_id in messages[:MAX_LATEST_EMAILS]:  # Limit to first MAX_LATEST_EMAILS emails
                msg_data = mail.fetch(msg_id, ["ENVELOPE"])
                envelope = msg_data[msg_id][b'ENVELOPE']

                # sender = envelope.from_  # e.g. "(Address(name=b'LinkedIn Job Alerts', route=None, mailbox=b'jobalerts-noreply', host=b'linkedin.com'),)"
                sender = envelope.from_[0]

                senderHost = sender.host.decode()
                senderMailbox = sender.mailbox.decode()

                subjectraw = envelope.subject.decode().lower()  # e.g. "=?UTF-8?Q?=E2=80=9Csoftware_developer=E2=80=9D:_Xero_-_Intermediate_Softw?= =?UTF-8?Q?are_Engineering_-_Product_&_Technology_and_more?=    "
                subject = str(make_header(decode_header(subjectraw)))

                isLinkedJobsEmail = senderHost == "linkedin.com" and senderMailbox.startswith("job") \
                    and subject.startswith('“software developer”:')
                if not isLinkedJobsEmail:
                    continue

                __printEmailHeaders(msg_id, sender, subject, senderMailbox, senderHost)
                jobs.append(subject)

                # emailBody = __readEmailBody(mail, msg_id)
                # __printEmailBody(msg_id, emailBody)
                ##asd TESTING
                # emailBody = __readEmailBody(mail, 582559)
                # emailBody = __readEmailBody(mail, 582555)
                # __printEmailBody(msg_id, emailBody)
                # break
                

                if subject.startswith('“software developer”:'):
                    linkedinJobsEmailCounter += 1

                if linkedinJobsEmailCounter >= MAX_LINKEDIN_JOBS_EMAILS:
                    break

            print()

    except Exception as e:
        print("Error:", e)

    return jobs


def __printEmailHeaders(msg_id, sender, subject, senderMailbox=None, senderHost=None):
    print()
    print(f"- Message ID: {msg_id}")
    print(f"  From: {sender}")
    print(f"  Subject: {subject}")
    print(f"  {senderMailbox} - {senderHost}")


def __printEmailBody(msg_id, emailBody):
    print()
    print("<" * BREAK_CHAR_COUNT)
    print(msg_id)
    print("EMAIL BODY:")
    print(emailBody)
    print(">" * BREAK_CHAR_COUNT)


def __readEmailBody(mail: IMAPClient, msg_id) -> str:
    EMAIL_MESSAGE_FORMAT = 'RFC822'
    EMAIL_MESSAGE_FORMAT_BINARY = b'RFC822'

    emailBodyResponse = mail.fetch([msg_id], [EMAIL_MESSAGE_FORMAT])
    emailBodyRaw = emailBodyResponse[msg_id][EMAIL_MESSAGE_FORMAT_BINARY]
    emailBodyParts = email.message_from_bytes(emailBodyRaw)
    emailBody = ""
    if emailBodyParts.is_multipart():
        for part in emailBodyParts.walk():
            if part.get_content_type() == "text/plain" and not part.get('Content-Disposition'):
                emailBody += __decodeEmailBody(part)
                break
    else:
        emailBody += __decodeEmailBody(emailBodyParts)

    return emailBody


def __decodeEmailBody(emailBodyParts) -> str:
    DEFAULT_CHARSET = 'utf-8'
    payload = emailBodyParts.get_payload(decode=True)
    decodedPayload = payload.decode(emailBodyParts.get_content_charset() or DEFAULT_CHARSET)
    return decodedPayload


if __name__ == "__main__":
    linkedinJobUrls = readLinkedinJobsEmail()
    print()
    print("Linkedin URLs:")
    for url in linkedinJobUrls:
        print(url)