import threading

import Pyro5.server
import Pyro5.api
from concurrent.futures import ThreadPoolExecutor
from util import States
import time
import random
Pyro5.config.COMMTIMEOUT = 0.5      # 1.5 seconds
Pyro5.config.MAX_RETRIES = 0      # attempt to retry 3 times before raise the exception

@Pyro5.server.expose
class Processo(object):
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.leaderId = None
        self.timeout = random.uniform(4, 10)
        print(f"[{self.name}]Timeout determinado {self.timeout}")
        self.iniciar_pyro()
        self.count_timeout = time.perf_counter()
        self.currentTerm = 0
        self.votedFor = None
        self.vote = 0
        self.log = []
        self.thread = threading.Thread(target=self._loop_daemon, daemon=True)
        self.thread.start()
        self.first_vote = True
        self.state = States.SEGUIDOR


    def iniciar_pyro(self):
        self.daemon = Pyro5.server.Daemon(host="localhost", port=self.port)
        self.uri = self.daemon.register(self, objectId=self.name)
        print(self.uri)

    def _loop_daemon(self):
        self.daemon.requestLoop()

    def fsm(self):
        time.sleep(2)
        while(True):
            match(self.state):
                case States.SEGUIDOR:
                    self.seguidor_state()

                case States.CANDIDATO:
                    self.currentTerm += 1                    
                    print(f"[{self.name}]CANDIDATO")
                    self.candidato_state()

                case States.LIDER:
                    print(f"[{self.name}] LIDER, currentTerm: {self.currentTerm}")
                    self.lider_state()

                case _:
                    print("não existe")

            time.sleep(0.1)

    def candidato_state(self):
        self.RequestVote()

        if(self.vote >= 3):
            self.publish_leader()
            self.state = States.LIDER
        else:
            self.count_timeout = time.perf_counter()
            print(f"[{self.name}]Candidatura falhou, voltando para seguidor")
            self.vote = 0
            self.state = States.SEGUIDOR

    def seguidor_state(self):
        end = time.perf_counter()
        value = end - self.count_timeout
        if(value > self.timeout):
            print(f"[{self.name}]: {value} > {self.timeout}")
            self.state = States.CANDIDATO
    
    def lider_state(self):
        self.AppendEntries()
       
    def aux_candidatura(self, processo, port):
        try:
            server = Pyro5.api.Proxy(f"PYRO:{processo}@localhost:{port}")
            if server.ReceiveRequestVote(self.currentTerm, self.name, 0, 0):
                self.vote += 1
        except Exception as e:
            print(f"Error calling ask_for_vote on {processo}:", e)
            
    def RequestVote(self):
        for i in range(1, 5):
            processo = f"processo{i}"
            porta = 9090 + i
            if processo == self.name:
                    continue
            self.aux_candidatura(processo, porta)

    def ReceiveRequestVote(self, termo, candidatoId, lastLogIndex, lastLogTerm):
        if(self.currentTerm < termo and self.state != States.LIDER):
            self.currentTerm = termo
            self.votedFor = None
        else:
            return False
        
        if(self.votedFor is None or self.votedFor == candidatoId):
            self.votedFor = candidatoId
            return True
        else:
            return False
        
    def aux_heartbeat(self, processo, port):
        try:
            server = Pyro5.api.Proxy(f"PYRO:{processo}@localhost:{port}")
            server.ReceiveAppendEntries(self.currentTerm, self.name)
        except Exception as e:
            print(f"Error calling receive_heartbeat on {processo}:", e)

    @Pyro5.server.oneway
    def AppendEntries(self):
        for i in range(1, 5):
            processo = f"processo{i}"
            porta = 9090 + i
            if processo == self.name:
                    continue
            self.aux_heartbeat(processo, porta)

    @Pyro5.server.oneway
    def ReceiveAppendEntries(self, termo, liderId):
        self.count_timeout = time.perf_counter()
        self.currentTerm = termo
        self.leaderId = liderId
        print(f"[{self.name}] HeartBeat Recebido")
        self.state = States.SEGUIDOR

   
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
