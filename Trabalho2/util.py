from enum import Enum

class States(Enum):
    IDLE = 0
    CANDIDATO = 1
    SEGUIDOR = 2
    LIDER = 3

class messageStatus(Enum):
    UNCOMMITED = 0
    COMMITED = 1