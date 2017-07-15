from django.test import TestCase, mock

from sms_app.app import SubscriptionApp
from sms_app.models import Subscriber
from sms_app.subscription_states import SubscriptionStates


class SmsAppTestCase(TestCase):
    _PHONE_NUMBER = "+11234567890"

    def test_spanish_reselect_lang(self):
        router = mock.Mock()
        app = SubscriptionApp(router)

        app.handle(self._incoming_msg("join"))
        app.handle(self._incoming_msg("2"))
        app.handle(self._incoming_msg("cambio de lengua"))

        subscriber = Subscriber.objects.get(phone_number=SmsAppTestCase._PHONE_NUMBER)
        self.assertEqual(subscriber.phone_number, SmsAppTestCase._PHONE_NUMBER)
        self.assertEqual(subscriber.language, "spa")
        self.assertEqual(subscriber.state, SubscriptionStates.SELECTING_LANG_STATE)

    def _incoming_msg(self, text):
        msg = mock.Mock()
        msg.connection.identity = SmsAppTestCase._PHONE_NUMBER
        msg.connections = [mock.Mock()]
        msg.text = text
        return msg
