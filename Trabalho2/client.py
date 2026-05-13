import Pyro5.api
import Pyro5.server
import threading
import questionary
import time


@Pyro5.server.expose
class client():
    def __init__(self):
        self.name = "cliente"
        self.port = 9089

        # Daemon do cliente para receber callback
        self.daemon = Pyro5.server.Daemon(host="localhost", port=self.port)
        self.uri = self.daemon.register(self, objectId=self.name)

        print(f"URI do cliente: {self.uri}")

        self.server = None
        self.uriServer = None

        self.thread = threading.Thread(target=self._loop_daemon, daemon=True)
        self.thread.start()

        self.refresh_leader()

    def _loop_daemon(self):
        self.daemon.requestLoop()

    def refresh_leader(self):
        nameserver = Pyro5.api.locate_ns()
        self.uriServer = nameserver.lookup("leader")
        self.server = Pyro5.api.Proxy(self.uriServer)

        self.server._pyroTimeout = 5

        print(f"Leader atual: {self.uriServer}")

    def kill_the_leader(self):
        try:
            self.refresh_leader()
            self.server.killMe()
            print("I killed the Leader")

            self.server = None
            self.uriServer = None

        except Exception as e:
            print("Error calling kill_the_leader:", e)

    def send_message(self, message):
        try:
            self.refresh_leader()
            self.server.ReceiveLog(message)

            print(f"Mensagem enviada para o leader: {message}")
            return

        except Exception as e:
            print(f"Erro ao enviar mensagem. Tentativa /3:", e)

    @Pyro5.server.oneway
    def receive_callback(self, message):
        print(f"\nRecebi a confirmação: {message}\n")


if __name__ == "__main__":
    client = client()

    print(f"uri: {client.uri}")

    while True:
        opcao = questionary.select(
            "Escolha uma opção:",
            choices=[
                "Enviar mensagem",
                "Matar leader",
                "Sair"
            ]
        ).ask()

        if opcao == "Enviar mensagem":
            mensagem = questionary.text(
                "Digite a mensagem que deseja enviar:"
            ).ask()

            if mensagem:
                client.send_message(mensagem)
            else:
                print("Mensagem vazia. Nada foi enviado.")

        elif opcao == "Matar leader":
            confirmar = questionary.confirm(
                "Tem certeza que deseja matar o leader?"
            ).ask()

            if confirmar:
                client.kill_the_leader()

        elif opcao == "Sair":
            print("Finish")
            break

        time.sleep(0.5)