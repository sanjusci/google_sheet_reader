# Create your service here.

__author__ = "Sanju Sci"
__email__ = "sanju.sci9@gmail.com"
__copyright__ = "Copyright 2019."

import os
import re
import smtplib
from utils.notification.email.smtp import SMTP
from jinja2 import Environment, FileSystemLoader
from utils.notification.notification_manager import NotificationManager, Parameters


class EmailManager(NotificationManager):

    EMAIL_REGX = re.compile('([\w\&\-\.\']+@(\w[\w\-]+\.)+[\w\-]+)')
    HTM_REGEX = re.compile('(^<!DOCTYPE html.*?>)')

    def __init__(self, templatedir='templates/email', *args, **kwargs):
        """
        Function __init__
        This function is used to initialize variables.

        :param templatedir:
          A templatedir that contains templeate directory name.
        """
        self.smtp = SMTP()
        self.connection = self.smtp._smtp_connect()
        if os.path.isdir(templatedir):
            self.templatedir = templatedir
        else:
            self.templatedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), templatedir)
        self.env = Environment(loader=FileSystemLoader(self.templatedir))

    def _mail_render(self, data, template):
        """
        Function _mail_render
        This function is used to render email content.

        :param data:
          A data that contains email data.
        :param template:
          A template that contains template name.

        :return:
          Return render message string.
        """
        try:
            template = template + ".html"
            print("Rendering template '{}'".format(template))
            text = self.env.get_template(template)
            message = text.render(data)
            return message
        except Exception as e:
            print("Rendering template error {}".format(e))

    def send_bulk(self, messages):
        """
        Function send_bulk
        This function is used to send bulk data

        :param messages:
          A messages that contains messages list.

        :return:
          Return processed messages count if email send else return Zero.
        """
        smtp = self.connection
        processed = 0
        for (recipient, subject, message, cc_email, bcc_email) in messages:
            try:
                self.smtp._smtp_send(
                    smtp=smtp, to=recipient,
                    subject=subject,
                    content=message,
                    cc=cc_email,
                    bcc=bcc_email,
                )
            except smtplib.SMTPException as e:
                print("Cannot send mail to {0}: {1}".format(recipient, e))
            else:
                processed += 1
        # smtp.quit()
        return processed

    def bulk_email(self, email_data):
        """
        Function bulk_email
        This function is used to send emails in bulk.

        :param email_data:
          An email_data that contains emails data list.

        :return:
          Return
        """
        email_list = []
        for edata in email_data:
            if not isinstance(edata, EmailParameters):
                print("Invalid emails parameters")
                continue
            try:
                email = edata.to
                cc_email = edata.cc
                bcc_email = edata.bcc
                subject = edata.subject
                data = edata.body
                template = edata.body["template"]
            except Exception as e:
                print("Cannot send mail to {}".format(e))
                continue
            if email is None:
                print("Email is empty!")
                continue
            for em in email:
                if self.EMAIL_REGX.match(em) is None:
                    print("Invalid email address!")
                    continue
            message = self._mail_render(data, template)
            email_list.append((email, subject, message, cc_email, bcc_email))
        if email_list:
            self.send_bulk(email_list)
        else:
            print("Cannot send mail to Email is empty!")

    def notify(self, *args, **kwargs):
        """
        Function notify
        This function is used to send notification to the given recipient.

        :param args:
          An args that contains argument tuples.
        :param kwargs:
          A kwargs that contains dict arguments

        :return:
          Return true.
        """
        try:
            self.bulk_email(args)
        except Exception as ex:
            print("<b>Email notification exception: {}</b>".format(ex))


class EmailParameters(Parameters):
    """
    Class EmailParameters
    This class is define default parameters
    """

    def __init__(self, to=(), cc=(), bcc=(), subject=None, body={}):
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.subject = subject
        self.body = body
