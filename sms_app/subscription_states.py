from transitions import Machine, State

from sms_app.asset_paths import *
from .messaging import Message


class SubscriptionStates(object):
    UNSUBSCRIBED_STATE = "unsubscribed"
    SELECTING_LANG_STATE = "selecting_language"
    COMPLETE_STATE = "complete"
    INITIAL_STATE = UNSUBSCRIBED_STATE

    _SRC = "source"
    _DST = "dest"
    _TRIGGER = "trigger"
    _AFTER = "after"
    _BEFORE = "before"

    _STATES = [
        UNSUBSCRIBED_STATE,
        SELECTING_LANG_STATE,
        COMPLETE_STATE
    ]

    _TRANSITIONS = [
        {
            _TRIGGER: "unknown_subscribe_msg",
            _SRC: UNSUBSCRIBED_STATE,
            _DST: UNSUBSCRIBED_STATE,
            _BEFORE: "_send_subscribe_help_msg"
        },
        {
            _TRIGGER: "subscribed",
            _SRC: UNSUBSCRIBED_STATE,
            _DST: SELECTING_LANG_STATE,
            _BEFORE: "_send_welcome_msg",
            _AFTER: "_send_lang_select_msg"
        },
        {
            _TRIGGER: "unknown_lang_selected",
            _SRC: SELECTING_LANG_STATE,
            _DST: SELECTING_LANG_STATE,
            _BEFORE: "_send_unsupported_lang_msg",
            _AFTER: "_send_lang_select_msg"
        },
        {
            _TRIGGER: "lang_selected",
            _SRC: SELECTING_LANG_STATE,
            _DST: COMPLETE_STATE,
            _AFTER: "_send_confirmation_msg"
        },
        {
            _TRIGGER: "unknown_complete_state_msg",
            _SRC: COMPLETE_STATE,
            _DST: COMPLETE_STATE,
            _AFTER: "_send_error_msg"
        },
        {
            _TRIGGER: "change_lang",
            _SRC: COMPLETE_STATE,
            _DST: SELECTING_LANG_STATE,
            _AFTER: "_send_lang_select_msg"
        },
        {
            _TRIGGER: "unsubscribed",
            _SRC: COMPLETE_STATE,
            _DST: UNSUBSCRIBED_STATE,
            _AFTER: "_send_unsubscribed_msg"
        },
    ]

    def __init__(self, initial_state, messenger):
        if initial_state not in SubscriptionStates._STATES:
            raise Exception("Unknown state: {}".format(initial_state))

        self.machine = Machine(
            model=self,
            states=SubscriptionStates._STATES,
            initial=initial_state,
            transitions=SubscriptionStates._TRANSITIONS
        )

        self.messenger = messenger

    def _send_subscribe_help_msg(self):
        self._send_msg(SUBSCRIBE_HELP_MSG_FILE)

    def _send_welcome_msg(self):
        self._send_msg(WELCOME_MSG_FILE)

    def _send_lang_select_msg(self):
        self._send_msg(LANG_SELECT_MSG_FILE)

    def _send_unsupported_lang_msg(self):
        self._send_msg(UNSUPPORTED_LANG_MSG_FILE)

    def _send_confirmation_msg(self):
        self._send_msg(CONFIRMATION_MSG_FILE)

    def _send_error_msg(self):
        self._send_msg(ERROR_MSG_FILE)

    def _send_unsubscribed_msg(self):
        self._send_msg(UNSUBSCRIBED_MSG_FILE)

    def _send_msg(self, filename):
        self.messenger.send(Message(filename))
