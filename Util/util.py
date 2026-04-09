from enum import Enum

def gerar_assinatura(dados, chave_privada):
    return "1234567890abcdef"

def verificar_assinatura(dados, assinatura, chave_publica):
    return True

class Voto(Enum):
    NEGATIVO = -1
    POSITIVO = 1