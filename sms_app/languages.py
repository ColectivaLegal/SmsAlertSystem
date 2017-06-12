class Language(object):
    DEFAULT_LANGUAGE = "en"

    # ISO 639-3 language codes
    ENGLISH = "eng"
    SPANISH = "spa"
    KOREAN = "kor"
    MANDARIN = "cmn"
    VIETNAMESE = "vie"

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
