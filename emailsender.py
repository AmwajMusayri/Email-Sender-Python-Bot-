# -*- coding: utf-8 -*-
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def create_email(sender_email, recipient_email, subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    if attachment_path and os.path.exists(attachment_path):
        filename = os.path.basename(attachment_path)
        try:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename= {filename}")
                msg.attach(part)
        except Exception as e:
            print(f"❌ Failed to attach file: {e}")
    return msg

def main():
    print("=== Automatic Email Sender Bot ===")
    
    # Configuration
    SENDER_EMAIL = "your_email@gmail.com"  # 👈 Enter your email here
    SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"  # 👈 Enter your 16-character App Password here
    
    # Check for email details from files
    if not os.path.exists("subject.txt") or not os.path.exists("message.txt"):
        print("\n⚠️ Files missing! Creating 'subject.txt' and 'message.txt'...")
        with open("subject.txt", "w", encoding="utf-8") as f: f.write("Put your subject here")
        with open("message.txt", "w", encoding="utf-8") as f: f.write("Put your multi-line message here")
        print("💡 Please edit these files, save them, then run the bot again!\n")
        return

    # Read Subject and Body
    with open("subject.txt", "r", encoding="utf-8") as f:
        subject = f.read().strip()
    with open("message.txt", "r", encoding="utf-8") as f:
        body = f.read()

    print(f"📝 Loaded Subject: {subject}")
    print("📝 Loaded Message with lines and spaces successfully!")

    attach_choice = input("\n📎 Do you want to attach a file? (yes/no): ").strip().lower()
    attachment_path = None
    if attach_choice in ['yes', 'y']:
        attachment_path = input("📂 Drag and drop the file here: ").strip().strip('"\'')

    try:
        print("\n⏳ Connecting to server...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("✅ Connected successfully!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    print("\n🚀 The Bot is ready!")
    print("--------------------------------------------------")
    while True:
        recipient = input("👤 Next Recipient Email (or type 'exit' to quit): ").strip()
        if recipient.lower() in ['exit', 'close', '']:
            break
        try:
            msg = create_email(SENDER_EMAIL, recipient, subject, body, attachment_path)
            server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
            print(f"✅ Successfully sent to: {recipient}\n")
        except Exception as e:
            print(f"❌ Error sending to {recipient}: {e}\n")
    server.quit()

if __name__ == "__main__":
    main()