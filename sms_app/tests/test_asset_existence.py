import os.path

from django.test import TestCase

from sms_app.asset_paths import *


class AssetExistenceTestCase(TestCase):
    def test_asset_existence(self):
        self.assertTrue(os.path.isfile(CONFIRMATION_MSG_FILE))
        self.assertTrue(os.path.isfile(LANG_SELECT_MSG_FILE))
        self.assertTrue(os.path.isfile(SUBSCRIBE_HELP_MSG_FILE))
        self.assertTrue(os.path.isfile(UNSUPPORTED_LANG_MSG_FILE))
        self.assertTrue(os.path.isfile(WELCOME_MSG_FILE))
        self.assertTrue(os.path.isfile(UNSUBSCRIBED_MSG_FILE))
        self.assertTrue(os.path.isfile(ERROR_MSG_FILE))
