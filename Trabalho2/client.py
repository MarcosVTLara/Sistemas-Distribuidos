import Pyro5.api

class client():
    def __init__(self):
        nameserver = Pyro5.api.locate_ns()
        self.uri = nameserver.lookup("leader")
        self.server = Pyro5.api.Proxy(self.uri)


    def hello_word(self):
        try:
            print(self.server.hello_word())
        except Exception as e:
            print("Error calling hello_word:", e)

    def hello_word_onew_way(self):
        try:
            self.server.hello_word_onew_way()
        except Exception as e:
            print("Error calling hello_word_onew_way:", e)

if __name__ == "__main__":
    client = client()
    client.hello_word()
    client.hello_word_onew_way()