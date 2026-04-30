from processo import Processo
from concurrent.futures import ThreadPoolExecutor

# from Trabalho2.processo2 import Processo2
import threading

def main():
    processo1 = Processo("processo1", 9091)
    processo2 = Processo("processo2", 9092)
    processo3 = Processo("processo3", 9093)
    processo4 = Processo("processo4", 9094)
    processo1.thread = threading.Thread(target=processo1.fsm, daemon=True)
    processo2.thread = threading.Thread(target=processo2.fsm, daemon=True)
    processo3.thread = threading.Thread(target=processo3.fsm, daemon=True)
    processo4.thread = threading.Thread(target=processo4.fsm, daemon=True)
    processo1.thread.start()
    processo2.thread.start()
    processo3.thread.start()
    processo4.thread.start()

    while(True):
        pass

if __name__ == "__main__":
    main()