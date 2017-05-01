from rapidsms.apps.base import AppBase

from .models import Subscriber


class SubscriptionApp(AppBase):
    _HELP_RESPONSE_FILENAME = "sms_app/assets/help_response.txt"

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
            msg.respond(file.read())
