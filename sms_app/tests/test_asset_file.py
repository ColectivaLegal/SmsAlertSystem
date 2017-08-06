import os.path

from django.test import TestCase

from sms_app.asset_file import *
from sms_app.languages import Language


class AssetExistenceTestCase(TestCase):
    def test_eng_asset_existence(self):
        lang = Language.ENGLISH
        self._test_lang_specific_files(lang)
        self._test_eng_only_files(lang)

    def test_default_asset_existence(self):
        lang = Language.DEFAULT_LANGUAGE
        self._test_lang_specific_files(lang)
        self._test_eng_only_files(lang)

    def test_spa_asset_existence(self):
        self._test_lang_specific_files(Language.SPANISH)

    def _test_lang_specific_files(self, lang):
        self.assertTrue(os.path.isfile(AssetFile(lang).confirmation_file()))
        self.assertTrue(os.path.isfile(AssetFile(lang).error_file()))
        self.assertTrue(os.path.isfile(AssetFile(lang).unsubscribe_file()))
        self.assertTrue(os.path.isfile(AssetFile(lang).action_alert_file()))
        self.assertTrue(os.path.isfile(AssetFile(lang).follow_up_file()))

    def _test_eng_only_files(self, lang):
        self.assertTrue(os.path.isfile(AssetFile(lang).lang_select_file()))
        self.assertTrue(os.path.isfile(AssetFile(lang).subscribe_help_file()))
        self.assertTrue(os.path.isfile(AssetFile(lang).unsupported_lang_file()))
        self.assertTrue(os.path.isfile(AssetFile(lang).welcome_file()))
