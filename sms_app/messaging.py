class Messenger(object):
    _MAX_MSG_LENGTH = 160

    def __init__(self, msg):
        self._msg = msg

    def send(self, message):
        msg_contents = message.contents()
        msg_pieces = [
            msg_contents[i: i + Messenger._MAX_MSG_LENGTH]
            for i in range(0, len(msg_contents), Messenger._MAX_MSG_LENGTH)
        ]

        for msg_pc in msg_pieces:
            self._msg.respond(msg_pc)


class Message(object):
    def __init__(self, filename):
        self._filename = filename

    def contents(self):
        with open(self._filename, "r") as file:
            return file.read()
