from enum import Enum
import json
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def gerar_assinatura(dados, chave_privada):
    privada = carregar_privada(chave_privada)
    conteudo = json.dumps(dados, sort_keys=True, separators=(',', ':')).encode()
    
    assinatura = privada.sign(
        conteudo,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )    
    
    return assinatura.hex()

def verificar_assinatura(dados, assinatura, chave_publica):
    publica = carregar_publica(chave_publica)
    try:
        mensagem = json.dumps(dados, sort_keys=True, separators=(',', ':')).encode()
        assinatura_bytes = bytes.fromhex(assinatura)

        publica.verify(
            assinatura_bytes,
            mensagem,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return True

    except InvalidSignature:
        return False

def carregar_privada(caminho):
    with open(caminho, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )

def carregar_publica(caminho):
    with open(caminho, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def carregar_env(caminho=".env"):
    """Carrega variáveis de ambiente de um arquivo .env (parser simples,
    sem dependências externas). Não sobrescreve variáveis já definidas."""
    if not os.path.exists(caminho):
        return
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            chave, valor = linha.split("=", 1)
            os.environ.setdefault(chave.strip(), valor.strip())
