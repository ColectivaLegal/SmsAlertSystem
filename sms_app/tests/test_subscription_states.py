from django.test import TestCase, mock

from sms_app.asset_paths import *
from sms_app.subscription_states import SubscriptionStates
from sms_app.languages import *


class SubscriptionStateTestCase(TestCase):

    def subscriber(self, state):
        sub = mock.Mock()
        sub.state = state
        sub.language = Language.DEFAULT_LANGUAGE
        sub.phone_number = "+1-123-456-7890"
        return sub

    def test_subscription_state_constructor(self):
        msgr = mock.Mock()
        SubscriptionStates(self.subscriber(SubscriptionStates.INITIAL_STATE), msgr)

    def test_subscribe_help(self):
        msgr = mock.Mock()
        state = SubscriptionStates(self.subscriber(SubscriptionStates.UNSUBSCRIBED_STATE), msgr)
        state.subscribe_help()

        assert msgr.send.call_count == 1
        self.assertEqual(msgr.send.call_args[0][0].contents(), self.read_file(SUBSCRIBE_HELP_MSG_FILE))

    def test_start_subscription(self):
        msgr = mock.Mock()
        state = SubscriptionStates(self.subscriber(SubscriptionStates.UNSUBSCRIBED_STATE), msgr)
        state.start_subscription()

        assert msgr.send.call_count == 2
        self.assertEqual(msgr.send.call_args_list[0][0][0].contents(), self.read_file(WELCOME_MSG_FILE))
        self.assertEqual(msgr.send.call_args_list[1][0][0].contents(), self.read_file(LANG_SELECT_MSG_FILE))

    def test_unknown_lang_selected(self):
        msgr = mock.Mock()
        state = SubscriptionStates(self.subscriber(SubscriptionStates.SELECTING_LANG_STATE), msgr)
        state.unknown_lang_selected()

        assert msgr.send.call_count == 2
        self.assertEqual(msgr.send.call_args_list[0][0][0].contents(), self.read_file(UNSUPPORTED_LANG_MSG_FILE))
        self.assertEqual(msgr.send.call_args_list[1][0][0].contents(), self.read_file(LANG_SELECT_MSG_FILE))

    def test_lang_selected(self):
        msgr = mock.Mock()
        state = SubscriptionStates(self.subscriber(SubscriptionStates.SELECTING_LANG_STATE), msgr)
        state.lang_selected("kor")

        assert msgr.send.call_count == 1
        self.assertEqual(msgr.send.call_args[0][0].contents(), self.read_file(CONFIRMATION_MSG_FILE))

    def test_complete_state_help(self):
        msgr = mock.Mock()
        state = SubscriptionStates(self.subscriber(SubscriptionStates.COMPLETE_STATE), msgr)
        state.complete_state_help()

        assert msgr.send.call_count == 1
        self.assertEqual(msgr.send.call_args[0][0].contents(), self.read_file(ERROR_MSG_FILE))

    def test_reselect_language(self):
        msgr = mock.Mock()
        state = SubscriptionStates(self.subscriber(SubscriptionStates.COMPLETE_STATE), msgr)
        state.reselect_language()

        assert msgr.send.call_count == 1
        self.assertEqual(msgr.send.call_args[0][0].contents(), self.read_file(LANG_SELECT_MSG_FILE))

    def test_end_subscription(self):
        msgr = mock.Mock()
        state = SubscriptionStates(self.subscriber(SubscriptionStates.COMPLETE_STATE), msgr)
        state.end_subscription()

        assert msgr.send.call_count == 1
        self.assertEqual(msgr.send.call_args[0][0].contents(), self.read_file(UNSUBSCRIBED_MSG_FILE))

    @staticmethod
    def read_file(filename):
        with open(filename, "r") as file:
            return file.read()
