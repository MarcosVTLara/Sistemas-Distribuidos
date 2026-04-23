import Pyro5.server
from util import States
import time
import random

@Pyro5.server.expose
class PyroService(object):
    def __init__(self):
        self.name = "processo4"
        self.state = States.SEGUIDOR
        self.timeout = random.uniform(0, 10)
        print(f"[{self.name}]Timeout determinado {self.timeout}")
        self.daemon = Pyro5.server.Daemon(host="localhost", port=9094)
        self.uri = self.daemon.register(PyroService, objectId=self.name)
        print(self.uri)
        self.count_timeout = time.perf_counter()
        self.termo = 1
        self.log
        self.daemon.requestLoop()
        self.first_vote = True

        self.server1 = Pyro5.api.Proxy("PYRO:processo1@localhost:9091")
        self.server2 = Pyro5.api.Proxy("PYRO:processo2@localhost:9092")
        self.server3 = Pyro5.api.Proxy("PYRO:processo3@localhost:9093")
        self.server4 = Pyro5.api.Proxy("PYRO:processo4@localhost:9094")




    def fsm(self):
        while(True):
            match(self.state):
                case States.SEGUIDOR:

                    print("Seguidor")
                    end = time.perf_counter()
                    if(end - self.counter_timeout > self.timeout):
                        self.state = States.CANDIDATO
                     ## sempre que receber heartbeat recomeça esse self.counter_timeout

                case States.CANDIDATO:
                    print("CANDIDATO")
                    self.send_candidatura()


                case States.LIDER:
                    print("LIDER")

                case _:
                    print("não existe")


    def send_candidatura(self):

        self.vote += self.server1.ask_for_vote(self.termo)        
        self.vote += self.server2.ask_for_vote(self.termo)
        self.vote += self.server3.ask_for_vote(self.termo)
        self.vote += self.server4.ask_for_vote(self.termo)
        if(self.vote >= 3):
        
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
        self.server1.receive_heartbeat()        
        self.server2.receive_heartbeat()
        self.server3.receive_heartbeat()
        self.server4.receive_heartbeat()
        
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


