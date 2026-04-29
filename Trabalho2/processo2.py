import threading

import Pyro5.server
import Pyro5.api
from Trabalho2.util import States
import time
import random

@Pyro5.server.expose
class Processo2(object):
    def __init__(self):
        self.name = "processo2"
        self.state = States.SEGUIDOR
        self.timeout = 10
        # self.timeout = random.uniform(1, 10)
        print(f"[{self.name}]Timeout determinado {self.timeout}")
        self.iniciar_pyro()
        self.count_timeout = time.perf_counter()
        self.termo = 1
        self.vote = 0
        # self.log
        self.thread = threading.Thread(target=self._loop_daemon, daemon=True)
        self.thread.start()
        self.first_vote = True

    def iniciar_pyro(self):
        self.daemon = Pyro5.server.Daemon(host="localhost", port=9092)
        self.uri = self.daemon.register(Processo2, objectId=self.name)
        print(self.uri)
        ns = Pyro5.core.locate_ns()
        ns.register(self.name, self.uri) # NameSever - ns

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
    
    def aux_candidatura(self, processo):
        try:
            nameserver = Pyro5.api.locate_ns()
            server = Pyro5.api.Proxy(nameserver.lookup(processo))
            self.vote += server.ask_for_vote(self.termo)
        except Exception as e:
            print(f"Error calling ask_for_vote on {processo}:", e)

    def send_candidatura(self):
        self.aux_candidatura("processo1")
        self.aux_candidatura("processo2")
        self.aux_candidatura("processo3")
        self.aux_candidatura("processo4")
        if(self.vote == 3):
            self.state = States.LIDER
        else:
            self.vote = 0
            self.state = States.SEGUIDOR
            print(f"[{self.name}]Candidatura falhou, voltando para seguidor")

    def ask_for_vote(self, termo):
        if(self.first_vote and self.termo <= termo):
            self.first_vote = False
            return 3
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