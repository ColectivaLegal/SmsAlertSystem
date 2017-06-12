from django.test import TestCase, mock

from sms_app.asset_paths import *
from sms_app.subscription_states import SubscriptionStates


class SubscriptionStateTestCase(TestCase):
    def test_subscription_state_constructor(self):
        msgr = mock.Mock()
        SubscriptionStates(SubscriptionStates.INITIAL_STATE, msgr)

    def test_unsubscribed_unknown_msg(self):
        msgr = mock.Mock()
        state = SubscriptionStates(SubscriptionStates.UNSUBSCRIBED_STATE, msgr)
        state.unknown_subscribe_msg()

        assert msgr.send.call_count == 1
        self.assertEqual(msgr.send.call_args[0][0].contents(), self.read_file(SUBSCRIBE_HELP_MSG_FILE))

    def test_unsubscribed_join_msg(self):
        msgr = mock.Mock()
        state = SubscriptionStates(SubscriptionStates.UNSUBSCRIBED_STATE, msgr)
        state.subscribed()

        assert msgr.send.call_count == 2
        self.assertEqual(msgr.send.call_args_list[0][0][0].contents(), self.read_file(WELCOME_MSG_FILE))
        self.assertEqual(msgr.send.call_args_list[1][0][0].contents(), self.read_file(LANG_SELECT_MSG_FILE))

    def test_lang_select_unknown_msg(self):
        msgr = mock.Mock()
        state = SubscriptionStates(SubscriptionStates.SELECTING_LANG_STATE, msgr)
        state.unknown_lang_selected()

        assert msgr.send.call_count == 2
        self.assertEqual(msgr.send.call_args_list[0][0][0].contents(), self.read_file(UNSUPPORTED_LANG_MSG_FILE))
        self.assertEqual(msgr.send.call_args_list[1][0][0].contents(), self.read_file(LANG_SELECT_MSG_FILE))

    def test_lang_select_success(self):
        msgr = mock.Mock()
        state = SubscriptionStates(SubscriptionStates.SELECTING_LANG_STATE, msgr)
        state.lang_selected()

        assert msgr.send.call_count == 1
        self.assertEqual(msgr.send.call_args[0][0].contents(), self.read_file(CONFIRMATION_MSG_FILE))

    def test_complete_unknown_msg(self):
        msgr = mock.Mock()
        state = SubscriptionStates(SubscriptionStates.COMPLETE_STATE, msgr)
        state.unknown_complete_state_msg()

        assert msgr.send.call_count == 1
        self.assertEqual(msgr.send.call_args[0][0].contents(), self.read_file(ERROR_MSG_FILE))

    def test_complete_change_lang_msg(self):
        msgr = mock.Mock()
        state = SubscriptionStates(SubscriptionStates.COMPLETE_STATE, msgr)
        state.change_lang()

        assert msgr.send.call_count == 1
        self.assertEqual(msgr.send.call_args[0][0].contents(), self.read_file(LANG_SELECT_MSG_FILE))

    def test_complete_unsubscribe(self):
        msgr = mock.Mock()
        state = SubscriptionStates(SubscriptionStates.COMPLETE_STATE, msgr)
        state.unsubscribed()

        assert msgr.send.call_count == 1
        self.assertEqual(msgr.send.call_args[0][0].contents(), self.read_file(UNSUBSCRIBED_MSG_FILE))

    @staticmethod
    def read_file(filename):
        with open(filename, "r") as file:
            return file.read()
