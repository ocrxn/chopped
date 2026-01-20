import smtplib, ssl
import getpass
import secrets
from config import MAIL_TOKEN

port = 465
smtp_server = 'smtp.gmail.com'
sender_email = "unh.chopped.ai@gmail.com"
receiver_email = "unh.chopped.ai@gmail.com"

def gen_code(length=6):
    return "".join(secrets.choice("23456789") for _ in range(length))

def connect_smtp(username):
    message = f"""Hello {username}
Here is your six digit code: {gen_code()}"""
    
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, MAIL_TOKEN)
        server.sendmail(sender_email, receiver_email, message)