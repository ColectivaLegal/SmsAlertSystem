from django.test import TestCase, mock

from sms_app.languages import *
from sms_app.subscription_states import SubscriptionStates


class SubscriptionStateTestCase(TestCase):
    def subscriber(self, state):
        sub = mock.Mock()
        sub.state = state
        sub.language = Language.ENGLISH
        sub.phone_number = "+11234567890"
        return sub

    def test_subscription_state_constructor(self):
        msgr = mock.Mock()
        SubscriptionStates(self.subscriber(SubscriptionStates.INITIAL_STATE), msgr)

    def test_subscribe_help(self):
        msgr = mock.Mock()
        state = SubscriptionStates(self.subscriber(SubscriptionStates.UNSUBSCRIBED_STATE), msgr)
        state.subscribe_help()

        assert msgr.send.call_count == 1
        self.assertEqual(
            msgr.send.call_args[0][0][0].contents(),
            self.read_file("sms_app/assets/eng/subscribe_help_msg.txt")
        )

    def test_start_subscription(self):
        msgr = mock.Mock()
        state = SubscriptionStates(self.subscriber(SubscriptionStates.UNSUBSCRIBED_STATE), msgr)
        state.start_subscription()

        assert msgr.send.call_count == 1
        self.assertEqual(
            msgr.send.call_args_list[0][0][0][0].contents(),
            self.read_file("sms_app/assets/eng/welcome_msg.txt")
        )
        self.assertEqual(
            msgr.send.call_args_list[0][0][0][1].contents(),
            self.read_file("sms_app/assets/eng/language_selection_msg.txt")
        )

    def test_unknown_lang_selected(self):
        msgr = mock.Mock()
        state = SubscriptionStates(self.subscriber(SubscriptionStates.SELECTING_LANG_STATE), msgr)
        state.unknown_lang_selected()

        assert msgr.send.call_count == 1
        self.assertEqual(
            msgr.send.call_args_list[0][0][0][0].contents(),
            self.read_file("sms_app/assets/eng/unsupported_lang_msg.txt")
        )
        self.assertEqual(
            msgr.send.call_args_list[0][0][0][1].contents(),
            self.read_file("sms_app/assets/eng/language_selection_msg.txt")
        )

    def test_lang_selected(self):
        msgr = mock.Mock()
        state = SubscriptionStates(self.subscriber(SubscriptionStates.SELECTING_LANG_STATE), msgr)
        state.lang_selected("spa")

        assert msgr.send.call_count == 1
        self.assertEqual(
            msgr.send.call_args[0][0][0].contents(),
            self.read_file("sms_app/assets/spa/confirmation_msg.txt")
        )

    def test_complete_state_help(self):
        msgr = mock.Mock()
        state = SubscriptionStates(self.subscriber(SubscriptionStates.COMPLETE_STATE), msgr)
        state.complete_state_help()

        assert msgr.send.call_count == 1
        self.assertEqual(
            msgr.send.call_args[0][0][0].contents(),
            self.read_file("sms_app/assets/eng/error_msg.txt")
        )

    def test_reselect_language(self):
        msgr = mock.Mock()
        state = SubscriptionStates(self.subscriber(SubscriptionStates.COMPLETE_STATE), msgr)
        state.reselect_language()

        assert msgr.send.call_count == 1
        self.assertEqual(
            msgr.send.call_args[0][0][0].contents(),
            self.read_file("sms_app/assets/eng/language_selection_msg.txt")
        )

    def test_end_subscription(self):
        msgr = mock.Mock()
        state = SubscriptionStates(self.subscriber(SubscriptionStates.COMPLETE_STATE), msgr)
        state.end_subscription()

        assert msgr.send.call_count == 1
        self.assertEqual(
            msgr.send.call_args[0][0][0].contents(),
            self.read_file("sms_app/assets/eng/unsubscribed_msg.txt")
        )

    @staticmethod
    def read_file(filename):
        with open(filename, "r") as file:
            return file.read()
