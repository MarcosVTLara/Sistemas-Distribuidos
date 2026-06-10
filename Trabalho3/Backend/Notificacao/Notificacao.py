import pika
import os
import json
import resend
import Util.util as util
import threading

util.carregar_env()

RABBIT_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
RESEND_FROM = os.environ.get("RESEND_FROM", "onboarding@resend.dev")
EMAIL_PADRAO = os.environ.get("LOJA_EMAIL_PADRAO", "")

resend.api_key = RESEND_API_KEY

class Notificacao:
    def __init__(self):
        params = pika.ConnectionParameters(host=RABBIT_HOST, heartbeat=0)
        self.connection_1 = pika.BlockingConnection(params)
        self.connection_2 = pika.BlockingConnection(params)
        self.connection_pub = pika.BlockingConnection(params)
        self.channel_1 = self.connection_1.channel()
        self.channel_1.exchange_declare(exchange='Promocoes', exchange_type='topic')
        self.channel_2 = self.connection_2.channel()
        self.channel_2.exchange_declare(exchange='Promocoes', exchange_type='topic')
        self.channel_pub = self.connection_pub.channel()
        self.channel_pub.exchange_declare(exchange='Promocoes', exchange_type='topic')
        self.pub_lock = threading.Lock()
        self.lista_promocoes = []

    def receive_publicada(self):
        result = self.channel_1.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel_1.queue_bind(exchange='Promocoes', queue=queue_name, routing_key="promocao.publicada")
        print(' [*] Waiting for logs. To exit press CTRL+C')
        def callback(ch, method, properties, body):
            obj = json.loads(body)
            print(f" [x] {obj}")
            if util.verificar_assinatura(obj["Data"], obj["Signature"], r".\publicas\Promocao_public.pem"):
                print(f" [x] Assinatura valida!")
                publicada = obj["Data"]["promocao"]
                self.lista_promocoes.append(publicada)
                self.enviar_categoria(publicada["promocao"], publicada["categoria"])
            else:
                print(f" [x] Assinatura inválida!")
        self.channel_1.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel_1.start_consuming()

    def receive_destaque(self):
        result = self.channel_2.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel_2.queue_bind(exchange='Promocoes', queue=queue_name, routing_key="promocao.destaque")
        print(' [*] Waiting for logs. To exit press CTRL+C')
        def callback(ch, method, properties, body):
            obj = json.loads(body)
            print(f" [x] {obj}")
            if util.verificar_assinatura(obj["Data"], obj["Signature"], r".\publicas\Ranking_public.pem"):
                print(f" [x] Assinatura valida!")
                nome = obj["Data"]["promocao"]
                promo = self.buscar_promocao(nome)
                categoria = promo["categoria"] if promo else None
                # 1) avisa os clientes legados via routing key de categoria
                self.enviar_categoria(f"hot deal {nome}", categoria)
                # 2) envia e-mail para a loja via API externa
                self.enviar_email(nome, promo)
                # 3) publica notificacao.hotdeal (consumido pelo Gateway -> SSE)
                self.enviar_hotdeal(nome, promo, categoria)
            else:
                print(f" [x] Assinatura inválida!")
        self.channel_2.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel_2.start_consuming()

    def buscar_promocao(self, promocao):
        for promocao_lista in self.lista_promocoes:
            if promocao_lista["promocao"] == promocao:
                return promocao_lista
        return None

    def verifica_categoria(self, promocao):
        promo = self.buscar_promocao(promocao)
        return promo["categoria"] if promo else None

    def enviar_hotdeal(self, nome, promo, categoria):
        dados = {
            "promocao": nome,
            "descricao": promo.get("descricao", "") if promo else "",
            "categoria": categoria,
        }
        message = {
            "Signature": util.gerar_assinatura(dados, r".\privadas\Notificacao_private.pem"),
            "Data": dados
        }
        body = json.dumps(message).encode('utf-8')
        with self.pub_lock:
            self.channel_pub.basic_publish(
                exchange='Promocoes', routing_key="notificacao.hotdeal", body=body)
        print(f" [x] Sent notificacao.hotdeal {dados}")

    def enviar_email(self, nome, promo):
        destino = (promo.get("email") if promo else "") or EMAIL_PADRAO
        if not destino:
            print(f" [!] Sem e-mail da loja para '{nome}' — pulando envio.")
            return
        if not RESEND_API_KEY:
            print(f" [!] RESEND_API_KEY não configurada — e-mail simulado para {destino} (hot deal: {nome})")
            return
        try:
            r = resend.Emails.send({
                "from": RESEND_FROM,
                "to": destino,
                "subject": f"Sua promoção virou HOT DEAL: {nome}",
                "html": f"<p>Parabéns! A promoção <strong>{nome}</strong> atingiu o limite de votos e agora é um hot deal.</p>",
            })
            print(f" [x] E-mail enviado para {destino}: {r}")
        except Exception as e:
            print(f" [!] Falha ao enviar e-mail para {destino}: {e}")

    def enviar_categoria(self, promocao, categoria):
        dados = {
            "promocao": promocao,
        }
        body = json.dumps(dados).encode('utf-8')
        routing_key_map = {
            "Eletrônicos": "promocao.eletronicos",
            "Roupas": "promocao.roupas",
            "Alimentos": "promocao.alimentos",
        }
        routing_key = routing_key_map.get(categoria)
        if routing_key is None:
            print(f" [!] Categoria desconhecida: {categoria}")
            return
        with self.pub_lock:
            self.channel_pub.basic_publish(
                exchange='Promocoes', routing_key=routing_key, body=body)
        print(f" [x] Sent {dados} - {categoria} ({routing_key})")

    def close(self):
        self.connection_1.close()
        self.connection_2.close()
        self.connection_pub.close()

if __name__ == "__main__":
    notificacao = Notificacao()
    thread_receive_publicada = threading.Thread(target=notificacao.receive_publicada)
    thread_receive_publicada.start()
    thread_receive_destaque = threading.Thread(target=notificacao.receive_destaque)
    thread_receive_destaque.start()
