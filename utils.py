import smtplib
from email.mime.text import MIMEText

from g3_dashboard import  settings

# import requests
# def send_simple_mail():
#     return requests.post(
#         "https://api.mailgun.net/v3/sandbox3c2172091a0d419e867ec7bf45185cdb.mailgun.org/messages",
#         auth=("api", "key-3d91be5330422b6a78f9e9d859010763"),
#         data={"from": "Mailgun Sandbox <postmaster@sandbox3c2172091a0d419e867ec7bf45185cdb.mailgun.org>",
#               "to": "gaurav <gaurav@madmachines.io>",
#               "subject": "Hello gaurav",
#               "text": "Congratulations gaurav, you just sent an email with "
#                       "Mailgun!  You are truly awesome!  You can see a record of this email in your "
#                       "logs: https://mailgun.com/cp/log .  You can send up to 300 emails/day from this "
#                       "sandbox server.  Next, you should add your own domain so you can send 10,000 "
#                       "emails/month for free."})


def send_mail(to, subject, msg_body):
    """
    Call to send email on users email address
    :param to:
    :param subject:
    :param msg_body:
    :return: True is user mail is send success
    """
    msg_content = msg_body
    message = MIMEText(msg_content, 'html')

    message['From'] = '3G DashBoard <sender@server>'
    message['To'] = to
    message['Cc'] = 'Gaurav Tyagi <gaurav@madmachines.io>'
    message['Subject'] = subject

    msg_full = message.as_string()

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    try:
        server.login('gaurav@madmachines.io', '@8447&&8447@')
        server.sendmail('gaurav@madmachines.io',
                        ['grvtyagi22@gmail.com'],
                        msg_full)
    except Exception as e:
        print(e.args)
    finally:
        server.quit()
