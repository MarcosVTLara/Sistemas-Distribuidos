import Pyro5.api

class client():
    def __init__(self):
        nameserver = Pyro5.api.locate_ns()
        self.uri = nameserver.lookup("leader")
        self.server = Pyro5.api.Proxy(self.uri)


    def kill_the_leader(self):
        try:
            self.server.killMe()
            print("I killed the Leader")
        except Exception as e:
            print("Error calling kill_the_leader:", e)


    def send_message(self, message):
        try:
            self.server.ReceiveLog(message)
        except Exception as e:
            print("Error calling send_message:", e)

if __name__ == "__main__":
    client = client()
    # client.kill_the_leader()
    client.send_message("6")