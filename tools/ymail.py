MAX_LINKEDIN_JOBS_EMAILS = 4

from dotenv import load_dotenv
import base64
import os
from imapclient import IMAPClient
from email.header import decode_header, make_header  # This is built-in, NO need for `pip install`.

load_dotenv()

YMAIL = os.getenv("YMAIL")
YAPP_PASSWORD = os.getenv("YAPP_PASSWORD") or "matamu" # https://login.yahoo.com/account/security?.lang=en-US&.intl=us&.src=yhelp → https://login.yahoo.com/myaccount/security/?.lang=en-US&.intl=us&.src=yhelp&.scrumb=qCwrl830s2G&anchorId=appPasswordCard

try:
    with IMAPClient("imap.mail.yahoo.com", ssl=True) as mail:
        mail.login(YMAIL, YAPP_PASSWORD)

        mail.select_folder("INBOX")

        messages = mail.search(["UNSEEN"])
        messages = sorted(messages, reverse=True)
        print(f"Unread Emails: {len(messages)}")

        # Fetch email headers
        if messages:
            linkedinJobsEmailCounter = 0

            # for msg_id in messages[:3]:  # Limit to first 3 emails
            for msg_id in messages[:12]:  # Limit to first 12 emails
                msg_data = mail.fetch(msg_id, ["ENVELOPE"])
                envelope = msg_data[msg_id][b'ENVELOPE']

                # sender = envelope.from_  # (Address(name=b'LinkedIn Job Alerts', route=None, mailbox=b'jobalerts-noreply', host=b'linkedin.com'),)
                sender = envelope.from_[0]

                senderHost = sender.host.decode()
                senderMailbox = sender.mailbox.decode()

                subjectraw = envelope.subject.decode().lower()
                subject = str(make_header(decode_header(subjectraw)))

                # print()
                # print(f"- From: {sender}")
                # print(f"  Subject: {subject}")

                isLinkedJobsEmail = senderHost == "linkedin.com" and senderMailbox.startswith("job") \
                    # and subject.startswith('“software developer”:')
                if isLinkedJobsEmail:
                    print()
                    print(f"- From: {sender}")
                    print(f"  Subject: {subject}")
                    print(f"  {senderMailbox} - {senderHost}")

                    if subject.startswith('“software developer”:'):
                        linkedinJobsEmailCounter += 1

                    if linkedinJobsEmailCounter >= MAX_LINKEDIN_JOBS_EMAILS:
                        break

                # - From: (Address(name=b'LinkedIn Job Alerts', route=None, mailbox=b'jobalerts-noreply', host=b'linkedin.com'),)
                #   Subject: =?UTF-8?Q?=E2=80=9Csoftware_developer=E2=80=9D:_Xero_-_Intermediate_Softw?= =?UTF-8?Q?are_Engineering_-_Product_&_Technology_and_more?=    

        print()

        exit(0)  #######
        print('inner')

        # from email_reader import read_email_body, get_email_body

        # print(read_email_body(get_email_body(mail, messages[0])))

except Exception as e:
    print("Error:", e)

print('outer')
