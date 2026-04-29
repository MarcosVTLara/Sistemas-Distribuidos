from Trabalho2.processo1 import Processo1
from Trabalho2.processo2 import Processo2
import threading

def main():
    processo1 = Processo1()
    processo2 = Processo2()
    processo1.thread = threading.Thread(target=processo1.fsm, daemon=True)
    processo2.thread = threading.Thread(target=processo2.fsm, daemon=True)
    processo2.thread.start()
    processo1.thread.start()
    while(True):
        pass

if __name__ == "__main__":
    main()