from enum import Enum
import json 
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


# private_key = rsa.generate_private_key(
#     public_exponent=65537,
#     key_size=2048
# )

# public_key = private_key.public_key()

# with open("Ranking_private.pem", "wb") as f:
#     f.write(
#         private_key.private_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PrivateFormat.PKCS8,
#             encryption_algorithm=serialization.NoEncryption()
#         )
#     )

# with open(f"Ranking_public.pem", "wb") as f:
#     f.write(
#         public_key.public_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PublicFormat.SubjectPublicKeyInfo
#         )
#     )