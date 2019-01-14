# Create your service here.

__author__ = "Sanju Sci"
__email__ = "sanju.sci9@gmail.com"
__copyright__ = "Copyright 2019."

from utils.commons import safe_invoke


class NotificationManager(object):

    def __init__(self,  *args, **kwargs):
        pass

    def notify(self, *args, **kwargs):
        pass

    @staticmethod
    def notify_sync(notif_mgr, *args, **kwargs):
        safe_invoke(notif_mgr.notify, *args)

    @classmethod
    def EMAIL(cls, *args, **kwargs):
        from utils.notification.email.email_manager import EmailManager
        return EmailManager(*args, **kwargs)


class Parameters(object):
    pass


__all__ = ["NotificationManager", "Parameters"]
