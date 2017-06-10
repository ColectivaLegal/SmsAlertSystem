from rapidsms.apps.base import AppBase

from .models import Subscriber


class SubscriptionApp(AppBase):
    """
    The SubscriptionApp is used to handle messages relating to a user's subscription status.
    """
    _HELP_RESPONSE_FILENAME = "sms_app/assets/help_response.txt"
    _MAX_MSG_LENGTH = 160

    def handle(self, msg):
        if msg.text.lower() == 'subscribe':
            phone_number = msg.connection.identity
            Subscriber.objects.create(phone_number=phone_number, language="EN")
            msg.respond("You have successfully subscribed to alerts. Text \"help\" for help.")
        elif msg.text.lower() == "unsubscribe":
            phone_number = msg.connection.identity
            Subscriber.objects.get(phone_number=phone_number).delete()
            msg.respond("You have successfully unsubscribed from alerts. Text \"help\" for help.")
        else:
            self._help(msg)
        return True

    def _help(self, msg):
        with open(SubscriptionApp._HELP_RESPONSE_FILENAME, "r") as file:
            file_txt = file.read()
            msg_pieces = [file_txt[i: i + SubscriptionApp._MAX_MSG_LENGTH] \
              for i in range(0, len(file_txt), SubscriptionApp._MAX_MSG_LENGTH)]

            for msg_pc in msg_pieces:
                msg.respond(msg_pc)
