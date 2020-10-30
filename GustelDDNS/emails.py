# coding=UTF-8
import smtplib
import sys

import config


from email.mime.text import MIMEText

username = config.readinifile("email","username")
password = config.readinifile("email","password")
email_sender = config.readinifile("email","from")
email_smtp = config.readinifile("email","smtp_server")
email_receiver = config.readinifile("email","to")


text_type = 'plain' # or 'html'
text = 'Sehr interessante Nachricht!'
msg = MIMEText(text, text_type, 'utf-8')
msg['Subject'] = 'Oi, ich glaub es geht!'
msg['From'] = email_sender
msg['To'] = email_receiver
server = smtplib.SMTP_SSL(email_smtp, 465)
server.login(username, password)
server.send_message(msg)
# or server.sendmail(msg['From'], msg['To'], msg.as_string())
server.quit()












