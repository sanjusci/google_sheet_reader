
__author__ = "Sanju Sci"
__email__ = "sanju.sci9@gmail.com"
__copyright__ = "Copyright 2019."

import os


class BaseConfig(object):

    SMTP_CONFIG = {
        'MAIL_SERVER': os.environ.get('MAIL_SERVER', 'smtp.googlemail.com'),
        'MAIL_SERVER_PORT': os.environ.get('MAIL_SERVER_PORT', 587),
        'MAIL_USE_TLS': False,
        'MAIL_USE_SSL': True,
        'MAIL_FROM_USER': os.environ.get('MAIL_FROM_USER', '!R&D - SOAR Services Team'),
        'MAIL_FROM_EMAIL': os.environ.get('MAIL_FROM_EMAIL', 'vivek.sharma@logrhythm.com'),
        'MAIL_USERNAME': os.environ.get('MAIL_USERNAME', 'testsrijan1@gmail.com'),
        'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD', 'srijan123'),
        'MAIL_TO': os.environ.get('MAIL_TO', 'user1@gmail.com'),
        'MAIL_CC': os.environ.get('MAIL_CC', 'user2@gmail.net'),
    }
