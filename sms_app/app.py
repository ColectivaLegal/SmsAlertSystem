import logging

from rapidsms.apps.base import AppBase

from .languages import Language, UnknownLanguageId
from .messaging import Messenger
from .models import Subscriber
from .subscription_states import SubscriptionStates


class SubscriptionApp(AppBase):
    """
    The SubscriptionApp is used to handle messages relating to a user's subscription status.
    """
    _DEFAULT_LANG = Language.ENGLISH

    def __init__(self, router):
        super().__init__(router)
        self._logger = logging.getLogger("rapidsms")

    def handle(self, msg):
        phone_number = msg.connection.identity
        subscriber, created = Subscriber.objects.get_or_create(
            phone_number=phone_number,
            defaults={
                "language": SubscriptionApp._DEFAULT_LANG,
                "state": SubscriptionStates.INITIAL_STATE
            }
        )
        self._logger.debug(
            "Current state of '{}' is '{}' with message '{}'".format(phone_number, subscriber.state, msg)
        )
        messenger = Messenger(msg)
        subscription_state = SubscriptionStates(subscriber, messenger)
        courier = SubscriptionCourier(messenger, subscription_state, subscriber)

        msg_text = msg.text.lower().strip()
        self._logger.debug(
            "Current state of '{}' is '{}' with message '{}'".format(phone_number, subscription_state.state, msg_text)
        )
        courier.receive(msg_text)

        return True


class SubscriptionCourier(object):
    _JOIN_MSG = "join"
    _CHG_LANG_MSG = "change language"
    _LEAVE_MSG = "leave"

    def __init__(self, messenger, subscription_state, subscriber):
        self._messenger = messenger
        self._subscription_state = subscription_state
        self._subscriber = subscriber
        self._logger = logging.getLogger("rapidsms")
        self._handled_msgs = {
            SubscriptionStates.UNSUBSCRIBED_STATE: self._on_unsubscribed_state,
            SubscriptionStates.SELECTING_LANG_STATE: self._on_select_lang_state,
            SubscriptionStates.COMPLETE_STATE: self._on_complete_state
        }

    def receive(self, msg_text):
        self._handled_msgs[self._subscription_state.state](msg_text)

    def _on_unsubscribed_state(self, msg_text):
        if msg_text == SubscriptionCourier._JOIN_MSG:
            self._subscription_state.start_subscription()
        else:
            self._subscription_state.subscribe_help()

    def _on_select_lang_state(self, msg_text):
        try:
            iso_code = Language.language(msg_text)
            self._subscription_state.lang_selected(iso_code)
        except UnknownLanguageId:
            self._subscription_state.unknown_lang_selected()

    def _on_complete_state(self, msg_text):
        if msg_text == SubscriptionCourier._CHG_LANG_MSG:
            self._subscription_state.reselect_language()
        elif msg_text == SubscriptionCourier._LEAVE_MSG:
            self._subscription_state.end_subscription()
        else:
            self._subscription_state.complete_state_help()