import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
load_dotenv()
mail_0 = os.environ['email0']
pw_0 = os.environ['emailpw0']

IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = mail_0
EMAIL_PASSWORD = pw_0

def get_unread_emails():
    try:
        # IMAPに接続
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")

        # 最新のメール50件を検索
        result, data = mail.search(None, "ALL")
        if result != "OK":
            print("Failed to search emails")
            return []
        
        mail_ids = data[0].split()
        if len(mail_ids) == 0:
            print("No emails found")
            return []

        # 最新の50件のメールIDを取得
        latest_mail_ids = mail_ids[-50:]
        
        unread_emails = []
        
        # 各メールIDについて処理
        for mail_id in latest_mail_ids:
            try:
                result, data = mail.fetch(mail_id, "(RFC822)")
                if result != "OK":
                    print(f"Failed to fetch email {mail_id}")
                    continue
                
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                # メールが未読であるかを確認
                result, flags = mail.fetch(mail_id, "(FLAGS)")
                if b'\\Seen' not in flags[0]:
                    # メールの件名を取得
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")

                    # メールの本文を取得
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            if "attachment" not in content_disposition:
                                if content_type == "text/plain":
                                    body = part.get_payload(decode=True).decode("utf-8")
                                    break
                    else:
                        body = msg.get_payload(decode=True).decode("utf-8")

                    unread_emails.append((subject, body))
            
            except Exception as e:
                print(f"Error processing email ID {mail_id}: {e}")
        
        mail.logout()
        return unread_emails

    except Exception as e:
        print(f"Error connecting to IMAP server: {e}")
        return []

# 未読メールを取得
unread_emails = get_unread_emails()

# 結果を表示
for subject, body in unread_emails:
    print(subject)
    print(body)
    print("-" * 40)