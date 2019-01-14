# Write your code here.

__author__ = "Sanju Sci"
__email__ = "sanju.sci9@gmail.com"
__copyright__ = "Copyright 2019."

import re
import smtplib
from config.base import BaseConfig as config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_CONFIG = config.SMTP_CONFIG


class SMTP(object):
    HTM_REGEX = re.compile('(^<!DOCTYPE html.*?>)')

    def __init__(self):
        """
        Function __init__
        This function is used to initialize the variables
        """
        self.smtp = SMTP_CONFIG['MAIL_SERVER']
        self.reply = SMTP_CONFIG['MAIL_FROM_EMAIL']
        self.smtp_login = SMTP_CONFIG['MAIL_USERNAME']
        self.smtp_pass = SMTP_CONFIG['MAIL_PASSWORD']
        self.smtp_port = SMTP_CONFIG['MAIL_SERVER_PORT']
        self.email_from = "{} <{}>".format(SMTP_CONFIG['MAIL_FROM_USER'], self.reply)

    def _smtp_connect(self):
        """
        Function _smtp_connect
        This function is used to create smtp connection.

        :return:
          Return smtp connection object else raise exception.
        """

        try:
            smtp = smtplib.SMTP(host=self.smtp, port=self.smtp_port)
            smtp.ehlo()
            smtp.starttls()
            print("SMTP connection established!")
        except Exception as e:
            print("Cannot connect with {0}: {1}".format(self.smtp, e))
        if self.smtp_login:
            try:
                smtp.login(self.smtp_login, self.smtp_pass)
                print("SMTP login successfully!")
            except smtplib.SMTPException as e:
                print("Cannot auth with {0} on {1}: {2}".format(self.smtp_login, self.smtp, e))
        return smtp

    def _smtp_send(self, smtp, subject, to, content, cc='', bcc='', email_from=''):
        """
        Function _smtp_send
        This function is used to send email to the recipient.

        :param smtp:
          A smtp that contains smtp object.
        :param recipient:
          A recipient that contains recipient email.
        :param subject:
          A subject that contains subject name.
        :param content:
          A content that contains content data.
        """
        try:
            msg = MIMEMultipart()
            if self.HTM_REGEX.match(content) is None:
                print("Sending text mail to {}".format(to))
                inner = MIMEText(content)
            else:
                print("Sending html mail to {}".format(to))
                inner = MIMEMultipart('alternative')
                inner.attach(MIMEText(content, 'html', 'utf-8'))
            msg.attach(inner)
            msg['From'] = email_from or self.email_from
            recipient = msg['To'] = ",".join(to) if isinstance(to, tuple) else to
            cc = msg['Cc'] = ",".join(cc) if isinstance(cc, tuple) else cc
            bcc = ",".join(bcc) if isinstance(bcc, tuple) else bcc
            msg['Subject'] = subject
            recipients = recipient.split(',') + cc.split(',') + bcc.split(',')
            smtp.sendmail(email_from or self.email_from, recipients, msg.as_string())
            print("SMTP mail successfully sent to {}!".format(recipients))
        except smtplib.SMTPException as e:
            print("Cannot send email error with: {}".format(e))
