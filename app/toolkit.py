import smtplib
from jinja2 import Environment, PackageLoader
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string
import random

def rand_gen(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def handle_email(toEmail,register_dict):
    fromEmail = "register@caurs.com"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Thank you for registering for CAURS!"
    msg['From'] = fromEmail
    msg['To'] = toEmail
    env = Environment(loader=PackageLoader(__name__, 'templates'))
    template = env.get_template('mail.tmpl')
    text =  template.render(form= register_dict)
    username = 'caurs'
    password = '663a765890d74d7a'

    part1 = MIMEText(text, 'plain')

    msg.attach(part1)

    s = smtplib.SMTP('smtp.sendgrid.net', 587)

    s.login(username, password)

    s.sendmail(fromEmail, toEmail, msg.as_string())

    s.quit()
