from transitions import Machine

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
            _TRIGGER: "subscribe_help",
            _SRC: UNSUBSCRIBED_STATE,
            _DST: UNSUBSCRIBED_STATE,
            _AFTER: "_subscribe_help"
        },
        {
            _TRIGGER: "start_subscription",
            _SRC: UNSUBSCRIBED_STATE,
            _DST: SELECTING_LANG_STATE,
            _AFTER: "_start_subscription"
        },
        {
            _TRIGGER: "unknown_lang_selected",
            _SRC: SELECTING_LANG_STATE,
            _DST: SELECTING_LANG_STATE,
            _AFTER: "_unknown_lang_selected"
        },
        {
            _TRIGGER: "lang_selected",
            _SRC: SELECTING_LANG_STATE,
            _DST: COMPLETE_STATE,
            _AFTER: "_lang_selected"
        },
        {
            _TRIGGER: "complete_state_help",
            _SRC: COMPLETE_STATE,
            _DST: COMPLETE_STATE,
            _AFTER: "_complete_state_help"
        },
        {
            _TRIGGER: "reselect_language",
            _SRC: COMPLETE_STATE,
            _DST: SELECTING_LANG_STATE,
            _AFTER: "_reselect_language"
        },
        {
            _TRIGGER: "end_subscription",
            _SRC: COMPLETE_STATE,
            _DST: UNSUBSCRIBED_STATE,
            _AFTER: "_end_subscription"
        },
    ]

    def __init__(self, subscriber, messenger):
        if subscriber.state not in SubscriptionStates._STATES:
            raise Exception("Unknown state: {}".format(subscriber.state))

        self._subscriber = subscriber
        self._machine = Machine(
            model=self,
            states=SubscriptionStates._STATES,
            initial=subscriber.state,
            transitions=SubscriptionStates._TRANSITIONS
        )
        self._messenger = messenger

    def _subscribe_help(self):
        self._send_msg(SUBSCRIBE_HELP_MSG_FILE)

    def _start_subscription(self):
        self._subscriber.state = SubscriptionStates.SELECTING_LANG_STATE
        self._subscriber.save()
        self._send_msg(WELCOME_MSG_FILE)
        self._send_msg(LANG_SELECT_MSG_FILE)

    def _unknown_lang_selected(self):
        self._send_msg(UNSUPPORTED_LANG_MSG_FILE)
        self._send_msg(LANG_SELECT_MSG_FILE)

    def _lang_selected(self, iso_code):
        self._subscriber.state = SubscriptionStates.COMPLETE_STATE
        self._subscriber.language = iso_code
        self._subscriber.save()
        self._send_msg(CONFIRMATION_MSG_FILE)

    def _complete_state_help(self):
        self._send_msg(ERROR_MSG_FILE)

    def _reselect_language(self):
        self._subscriber.state = SubscriptionStates.SELECTING_LANG_STATE
        self._subscriber.save()
        self._send_msg(LANG_SELECT_MSG_FILE)

    def _end_subscription(self):
        self._subscriber.state = SubscriptionStates.UNSUBSCRIBED_STATE
        self._send_msg(UNSUBSCRIBED_MSG_FILE)

    def _send_msg(self, filename):
        self._messenger.send(Message(filename))
