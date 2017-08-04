class Language(object):
    # ISO 639-3 language codes
    ENGLISH = "eng"
    SPANISH = "spa"
    KOREAN = "kor"
    MANDARIN = "cmn"
    VIETNAMESE = "vie"

    DEFAULT_LANGUAGE = ENGLISH

    SUPPORTED_LANGUAGES = [
        ENGLISH,
        SPANISH
    ]

    _language_id = {
        "1": ENGLISH,
        "2": SPANISH,
        "3": KOREAN,
        "4": MANDARIN,
        "5": VIETNAMESE
    }

    @staticmethod
    def language(lang_id):
        try:
            iso_code = Language._language_id[lang_id]
            return iso_code
        except KeyError:
            raise UnknownLanguageId("Unable to determine language with id: {}".format(lang_id))


class UnknownLanguageId(Exception):
    pass


class MessageContent(object):
    _JOIN_PHRASES = [
        "join",
        "suscribirse"
    ]
    _CHG_LANG_PHRASES = [
        "change language",
        "cambio de lengua"
    ]
    _LEAVE_PHRASES = [
        "leave",
        "abandonar"
    ]

    def __init__(self, msg):
        self._msg = msg

    def is_join_msg(self):
        return self._msg in MessageContent._JOIN_PHRASES

    def is_change_lang_msg(self):
        return self._msg in MessageContent._CHG_LANG_PHRASES

    def is_leave_msg(self):
        return self._msg in MessageContent._LEAVE_PHRASES
