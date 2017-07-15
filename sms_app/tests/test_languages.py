from django.test import TestCase

from sms_app.languages import Language, UnknownLanguageId, MessageContent


class LanguagesTestCase(TestCase):
    def test_supported_language_index(self):
        iso_code = Language.language("1")
        self.assertEqual(iso_code, "eng")

    def test_unsupported_language_index(self):
        try:
            Language.language("100")
            self.fail()
        except UnknownLanguageId:
            pass


class MessageContentTestCase(TestCase):
    def test_eng_join(self):
        msg = "join"
        self.assertTrue(MessageContent(msg).is_join_msg())
        self.assertFalse(MessageContent(msg).is_change_lang_msg())
        self.assertFalse(MessageContent(msg).is_leave_msg())

    def test_spa_change_lang(self):
        msg = "cambio de lengua"
        self.assertFalse(MessageContent(msg).is_join_msg())
        self.assertTrue(MessageContent(msg).is_change_lang_msg())
        self.assertFalse(MessageContent(msg).is_leave_msg())

    def test_spa_leave(self):
        msg = "abandonar"
        self.assertFalse(MessageContent(msg).is_join_msg())
        self.assertFalse(MessageContent(msg).is_change_lang_msg())
        self.assertTrue(MessageContent(msg).is_leave_msg())

    def test_garbage(self):
        msg = "garbage"
        self.assertFalse(MessageContent(msg).is_join_msg())
        self.assertFalse(MessageContent(msg).is_change_lang_msg())
        self.assertFalse(MessageContent(msg).is_leave_msg())
