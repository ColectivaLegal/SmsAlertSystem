import codecs


class Messenger(object):
    _MAX_MSG_LENGTH = 70
    _SPLIT_LENGTH = _MAX_MSG_LENGTH - len("(1/1) ")

    def __init__(self, msg):
        self._msg = msg

    def send(self, messages):
        msg_pieces = self._split_msg("\n".join([msg.contents() for msg in messages]))

        for msg_pc in msg_pieces:
            self._msg.respond(msg_pc)

    def _split_msg(self, msg_contents):
        if len(msg_contents) <= Messenger._MAX_MSG_LENGTH:
            return [msg_contents]

        msg_pieces = [
            msg_contents[i: i + Messenger._SPLIT_LENGTH]
            for i in range(0, len(msg_contents), Messenger._SPLIT_LENGTH)
        ]
        enumed_msg_pieces = [
            "({}/{}) {}".format(i + 1, len(msg_pieces), msg_pieces[i])
            for i in range(0, len(msg_pieces))
        ]

        return enumed_msg_pieces


class Message(object):
    def __init__(self, filename):
        self._filename = filename

    def contents(self):
        with codecs.open(self._filename, "r", "utf-8") as file:
            return file.read()
