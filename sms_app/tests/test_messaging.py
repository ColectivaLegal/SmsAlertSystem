from django.test import TestCase, mock

from sms_app.messaging import Message, Messenger


class MessageTestCase(TestCase):
    def test_message_contents(self):
        msg = Message("sms_app/tests/msg_file.txt")
        self.assertEqual(msg.contents(), "HERE'S JOHNNY!")


class MessengerTestCase(TestCase):
    def test_messenger_send(self):
        received_msg = mock.Mock()
        msgr = Messenger(received_msg)

        msg = mock.Mock()
        msg_text = "Shake it fast, WATCH YO SELF"
        msg.contents = mock.Mock(return_value=msg_text)
        msgr.send(msg)

        received_msg.respond.assert_any_call(msg_text)
