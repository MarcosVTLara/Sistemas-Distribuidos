import threading

import Pyro5.server
import Pyro5.api
from concurrent.futures import ThreadPoolExecutor
from util import States, messageStatus
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
        self.nextIndex = [0, 0, 0, 0]
        self.matchIndex = [0, 0, 0, 0]
        self.indexUncommited = None
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

                case States.IDLE:
                    print(f"[{self.name}] Estou morto")

                case _:
                    print("não existe")

            time.sleep(0.5)

    def candidato_state(self):
        self.RequestVote()
        self.vote += 1
        self.votedFor = self.name
        if(self.vote > 2):
            self.publish_leader()
            self.state = States.LIDER
        else:
            self.count_timeout = time.perf_counter()
            print(f"[{self.name}]Candidatura falhou(votos:{self.vote}), voltando para seguidor")
            self.vote = 0
            self.state = States.SEGUIDOR

    def seguidor_state(self):
        end = time.perf_counter()
        value = end - self.count_timeout
        if(value > self.timeout):
            print(f"[{self.name}]: {value} > {self.timeout}")
            self.state = States.CANDIDATO
    
    def lider_state(self):
        # if self.newLog:
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
        print(f"Request vote of {candidatoId} with termo {termo}")
        if termo < self.currentTerm:
            return False
        if termo > self.currentTerm:
            self.currentTerm = termo
            self.votedFor = None
            self.state = States.SEGUIDOR
            self.count_timeout = time.perf_counter()
        
        if(self.votedFor is None or self.votedFor == candidatoId):
            print('self.votedFor', self.votedFor)
            self.votedFor = candidatoId
            print()
            print(f"[{self.name}]: Votei no {candidatoId}, termo: {termo}")
            return True
        else:
            return False
        
    def aux_heartbeat(self, processo, port):
        try:
            log = self.log[self.indexUncommited] if self.indexUncommited is not None and self.indexUncommited < len(self.log) else None
            if log:
                print(f"Send Log: {log}")
            server = Pyro5.api.Proxy(f"PYRO:{processo}@localhost:{port}")
            response = server.ReceiveAppendEntries(
                self.currentTerm, self.name, None, None, log, self.indexUncommited
            )
            return response
        except Exception as e:
            print(f"Error calling ReceiveAppendEntries on {processo}:", e)
            return False

    def AppendEntries(self):
        somatorio = 0
        for i in range(1, 5):
            processo = f"processo{i}"
            porta = 9090 + i
            if processo == self.name:
                continue
            response = self.aux_heartbeat(processo, porta)
            if response:
                somatorio += 1

        # Maioria confirmou → commita e avança
        if somatorio > 2 and self.indexUncommited is not None and self.indexUncommited < len(self.log):
            self.log[self.indexUncommited]["status"] = messageStatus.COMMITED
            print(f"[{self.name}] Log comitado: {self.log[self.indexUncommited]}")
            self.indexUncommited += 1

    def ReceiveAppendEntries(self, termo, liderId, prevLogIndex, prevLogTerm, entries, leaderCommit):
        if termo < self.currentTerm:
            return False

        self.count_timeout = time.perf_counter()
        self.state = States.SEGUIDOR
        self.currentTerm = termo
        self.votedFor = None
        self.leaderId = liderId
        print(f"[{self.name}] HeartBear Recebido")
        # Recebeu uma entrada nova (evita duplicata checando o index)
        if entries is not None:
            if leaderCommit is not None and leaderCommit >= len(self.log):
                self.log.append({
                    "message": entries["message"],
                    "termo": entries["termo"],
                    "status": messageStatus.UNCOMMITED
                })
                print(f"[{self.name}] Log recebido: {entries}")

        # Líder já commitou → follower commita também e avança
        if leaderCommit is not None and leaderCommit < len(self.log):
            if self.log[leaderCommit]["status"] != messageStatus.COMMITED:
                self.log[leaderCommit]["status"] = messageStatus.COMMITED
                print(f"[{self.name}] Log comitado por líder: {self.log[leaderCommit]}")
        
        if leaderCommit is not None:
            self.indexUncommited = leaderCommit

        return True

   
    @Pyro5.server.oneway
    def receive_info(self, info):
        print(f"[{self.name}] Client info")
        self.send_processos(info)

    @Pyro5.server.oneway
    def ReceiveLog(self, message):
        print(f"[{self.name}] Recebi log: {message}")
        if len(self.log) == 0:
            self.indexUncommited = 0
        self.log.append({
            "message": message,
            "termo": self.currentTerm,
            "status": messageStatus.UNCOMMITED
        })
        print(f"[{self.name}] Log atual: {self.log}")




    @Pyro5.server.oneway
    def killMe(self):
        self.state = States.IDLE

    def receive_commit():
        ## if commits >= 3
        ## self.log.append(info)
        ## send_commit_seguidores()
        print()
    
    def publish_leader(self):
        ns = Pyro5.core.locate_ns()
        ns.register("leader", self.uri)
        print(f"DECLARE LEADER {self.uri}")

if __name__ == "__main__":
    import sys

    nome = sys.argv[1]
    porta = int(sys.argv[2])

    processo = Processo(nome, porta)

    processo.fsm()