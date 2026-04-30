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
        self.state = States.SEGUIDOR
        self.timeout = random.uniform(2, 10)
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
        self.daemon = Pyro5.server.Daemon(host="localhost", port=self.port)
        self.uri = self.daemon.register(self, objectId=self.name)
        print(self.uri)

    def _loop_daemon(self):
        print("Daemon rodando em thread separada...")
        self.daemon.requestLoop()

    def fsm(self):
        time.sleep(2)
        while(True):
            match(self.state):
                case States.SEGUIDOR:
                    self.seguidor_state()

                case States.CANDIDATO:
                    print(f"[{self.name}]CANDIDATO")
                    self.candidato_state()

                case States.LIDER:
                    print(f"[{self.name}] LIDER")
                    self.lider_state()

                case _:
                    print("não existe")

            time.sleep(0.05)
    
    def aux_candidatura(self, processo, port):
        try:
            server = Pyro5.api.Proxy(f"PYRO:{processo}@localhost:{port}")
            self.vote += server.ask_for_vote(self.termo)
        except Exception as e:
            print(f"Error calling ask_for_vote on {processo}:", e)

    def candidato_state(self):
        for i in range(1, 5):
            with ThreadPoolExecutor(max_workers=3) as executor:
                processo = f"processo{i}"
                porta = 9090 + i
                if processo == self.name:
                    continue
                executor.submit(self.aux_candidatura, processo, porta)

        if(self.vote >= 3):
            self.state = States.LIDER
            self.publish_leader()
        else:
            self.vote = 0
            self.state = States.SEGUIDOR
            self.count_timeout = time.perf_counter()
            print(f"[{self.name}]Candidatura falhou, voltando para seguidor")

    def seguidor_state(self):
        end = time.perf_counter()
        value = end - self.count_timeout
        if(value > self.timeout):
            print(f"[{self.name}]: {value} > {self.timeout}")
            self.state = States.CANDIDATO
    
    def lider_state(self):
        self.send_heartbeat()
       
    def ask_for_vote(self, termo):
        if(self.first_vote and self.termo <= termo):
            self.first_vote = False
            return 1
        else:
            return 0

    def aux_heartbeat(self, processo, port):
        try:
            server = Pyro5.api.Proxy(f"PYRO:{processo}@localhost:{port}")
            server.receive_heartbeat()
        except Exception as e:
            print(f"Error calling receive_heartbeat on {processo}:", e)

    @Pyro5.server.oneway
    def send_heartbeat(self):
        for i in range(1, 5):
            processo = f"processo{i}"
            porta = 9090 + i
            if processo == self.name:
                    continue
            self.aux_heartbeat(processo, porta)
            # with ThreadPoolExecutor(max_workers=3) as executor:

            #     executor.submit(self.aux_heartbeat, processo, porta)

    @Pyro5.server.oneway
    def receive_heartbeat(self):
        self.count_timeout = time.perf_counter()
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


if __name__ == "__main__":
    processo = Processo("processo1", 9091)
    processo.fsm()