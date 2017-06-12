from django.test import TestCase

from sms_app.languages import Language, UnknownLanguageId


class LanguagesTestCase(TestCase):
    def test_supported_language_index(self):
        iso_code = Language.language("1")
        self.assertEqual(iso_code, 'eng')

    def test_unsupported_language_index(self):
        try:
            Language.language("100")
            self.fail()
        except UnknownLanguageId:
            pass
