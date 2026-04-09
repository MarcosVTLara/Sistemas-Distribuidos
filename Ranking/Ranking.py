#!/usr/bin/env python
import pika
import json
import Util.util as util
import threading

class Ranking:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='Promocoes', exchange_type='direct')
        self.ranking = {}
        self.hot_deal_value = 5

    def receive_voto(self):
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange='Promocoes', queue=queue_name, routing_key="voto")
        print(' [*] Waiting for logs. To exit press CTRL+C')
        def callback(ch, method, properties, body):
            obj = json.loads(body)
            print(f" [x] {obj}")
            if util.verificar_assinatura(obj["Data"], obj["Signature"], "chave_publica"):
                print(f" [x] Assinatura valida!")
                self.contabilizar_votos(obj["Data"])
            else:
                print(f" [x] Assinatura inválida!")

        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def contabilizar_votos(self, data):
        promocao = data["promocao"]
        voto = data["voto"]
        if promocao not in self.ranking:
            self.ranking[promocao] = 0
        if voto == "Positivo":
            self.ranking[promocao]  = self.ranking[promocao] + 1
        elif voto == "Negativo":
            self.ranking[promocao]  = self.ranking[promocao] - 1

        print(f" [x] Ranking atualizado: {self.ranking}")
        if self.ranking[promocao] >= self.hot_deal_value:
            print(f" [x] Promoção {promocao} é um hot deal!")

    def enviar_destaque(self, promocao_destaque):
        dados = { 
            "Data":{
                "destaque": promocao_destaque,
            }
        }
        message = {
            "Signature": util.gerar_assinatura(dados, "chave_privada"),
            "Data": dados["Data"]
        }
        body = json.dumps(message).encode('utf-8')
        self.channel.basic_publish(exchange='Promocoes', routing_key="destaque", body=body)
        print(f" [x] Sent {message}")

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    Ranking = Ranking()
    thread_receive = threading.Thread(target=Ranking.receive_voto)
    thread_receive.start()
