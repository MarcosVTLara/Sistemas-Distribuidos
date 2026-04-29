import threading

import Pyro5.server
import Pyro5.api
from Trabalho2.util import States
import time
import random

@Pyro5.server.expose
class Processo1(object):
    def __init__(self):
        self.name = "processo1"
        self.state = States.SEGUIDOR
        self.timeout = random.uniform(0, 10)
        print(f"[{self.name}]Timeout determinado {self.timeout}")
        self.daemon = Pyro5.server.Daemon(host="localhost", port=9091)
        self.uri = self.daemon.register(Processo1, objectId=self.name)
        print(self.uri)
        self.vote = 0
        ns = Pyro5.core.locate_ns()
        ns.register(self.name, self.uri) # NameSever - ns
        self.count_timeout = time.perf_counter()
        self.termo = 1
        # self.log
                # inicia thread separada
        self.thread = threading.Thread(target=self._loop_daemon, daemon=True)
        self.thread.start()
        # self.daemon.requestLoop()
        self.first_vote = True
        # self.server2 = Pyro5.api.Proxy(nameserver.lookup("processo2"))
        # self.server3 = Pyro5.api.Proxy(nameserver.lookup("processo3"))
        # self.server4 = Pyro5.api.Proxy(nameserver.lookup("processo4"))

        # self.server1 = Pyro5.api.Proxy("PYRO:processo1@localhost:9091")
        # self.server3 = Pyro5.api.Proxy("PYRO:processo3@localhost:9093")
        # self.server4 = Pyro5.api.Proxy("PYRO:processo4@localhost:9094")



    def _loop_daemon(self):
        print("Daemon rodando em thread separada...")
        self.daemon.requestLoop()

    def fsm(self):
        while(True):
            match(self.state):
                case States.SEGUIDOR:

                    # print("Seguidor")
                    end = time.perf_counter()
                    if(end - self.count_timeout > self.timeout):
                        self.state = States.CANDIDATO
                     ## sempre que receber heartbeat recomeça esse self.counter_timeout

                case States.CANDIDATO:
                    print("CANDIDATO")
                    self.send_candidatura()


                case States.LIDER:
                    self.send_heartbeat()
                    print("LIDER")

                case _:
                    print("não existe")

    def send_candidatura(self):
        nameserver = Pyro5.api.locate_ns()
        # self.vote += self.server1.ask_for_vote(self.termo)
        self.server2 = Pyro5.api.Proxy(nameserver.lookup("processo2"))
        self.vote += self.server2.ask_for_vote(self.termo)
        # self.vote += self.server3.ask_for_vote(self.termo)
        # self.vote += self.server4.ask_for_vote(self.termo)
        # if(self.vote >= 3):
        if(self.vote == 1):
            self.state = States.LIDER
        else:
            print()
            # Recomeça a canditadura?
            # se receber um heartbeat volta para seguidor?

    def ask_for_vote(self, termo):
        if(self.first_vote and self.termo <= termo):
            self.first_vote = False
            return 1
        else:
            return 0
        
    @Pyro5.server.oneway
    def send_heartbeat(self):
        # self.server1.receive_heartbeat()        
        self.server2.receive_heartbeat()
        # self.server3.receive_heartbeat()
        # self.server4.receive_heartbeat()
        
    @Pyro5.server.oneway
    def receive_heartbeat(self):
        self.count_timeout = time.perf_counter()
        print(f"[{self.name}] HeartBeat Recebido, Contagem reniciada")
        return
    
    @Pyro5.server.oneway
    def receive_info(self, info):
        print(f"[{self.name}] Client info")
        self.send_processos(info)

    def receive_commit():
        ## if commits >= 3
        ## self.log.append(info)
        ## send_commit_seguidores()
        print()
    
    def publish_leader(self):
        ns = Pyro5.core.locate_ns()
        ns.register("leader", self.uri)

if __name__ == "__main__":
    name = PyroService()
    name.fsm()