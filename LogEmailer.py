import smtplib, ssl
from Config import auth
file = open('nba.log', 'r')

TEXT = file.read()

file.close()

SUBJECT = 'NBA Logs'
smtp_server = 'smtp.gmail.com'
port = 587
from_auth = (auth['from_address'], auth['password'])
to_addr = auth['to_address']
message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
context = ssl.create_default_context()

try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(from_auth[0], from_auth[1])
    server.sendmail(from_addr=from_auth[0], to_addrs=to_addr, msg=message)
except Exception as e:
    print(f"error: {e}")
finally:
    # noinspection PyUnboundLocalVariable
    server.quit()
