class FakeRadio:
    def __init__(self, messages: list[str] = None):
        if messages == None:
            messages = []
        self.messages = messages

    def receive(self):
        try:
            return self.messages.pop()
        except IndexError:
            return ""
