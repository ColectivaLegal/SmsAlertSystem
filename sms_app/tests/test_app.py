from django.test import TestCase, mock

from sms_app.app import SubscriptionApp, SubscriptionCourier
from sms_app.subscription_states import SubscriptionStates


class SubscriptionAppTestCase(TestCase):
    def test_initialization(self):
        router = mock.Mock()
        SubscriptionApp(router)

    def test_unknown_msg_handling(self):
        msg = mock.Mock()
        msg.connection.identity = "+11234567890"
        msg.connections = [mock.Mock()]
        msg.text = "some RANDOM garbage"

        router = mock.Mock()
        app = SubscriptionApp(router)

        app.handle(msg)


class SubscriptionCourierTestCase(TestCase):
    def test_unknown_msg_handling(self):
        messenger = mock.Mock()
        subscription_state = mock.Mock()
        subscription_state.state = SubscriptionStates.UNSUBSCRIBED_STATE
        subscriber = mock.Mock()

        courier = SubscriptionCourier(messenger, subscription_state, subscriber)
        courier.receive("Keanu Reeves is a great actor")

        assert subscription_state.subscribe_help.call_count == 1

    def test_unsupported_lang_selection(self):
        messenger = mock.Mock()
        subscription_state = mock.Mock()
        subscription_state.state = SubscriptionStates.SELECTING_LANG_STATE
        subscriber = mock.Mock()

        courier = SubscriptionCourier(messenger, subscription_state, subscriber)
        courier.receive("?")

        assert subscription_state.unknown_lang_selected.call_count == 1

    def test_reselect_lang(self):
        messenger = mock.Mock()
        subscription_state = mock.Mock()
        subscription_state.state = SubscriptionStates.COMPLETE_STATE
        subscriber = mock.Mock()

        courier = SubscriptionCourier(messenger, subscription_state, subscriber)
        courier.receive("cambio de lengua")

        assert subscription_state.reselect_language.call_count == 1
