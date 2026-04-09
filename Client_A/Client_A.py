#!/usr/bin/env python
import pika
import json
import Util.util as util
import threading

class Client_A:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='Promocoes', exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange='Promocoes', queue=queue_name, routing_key="voto") # TROCAR VOTO POR CATEGORIA
        print(' [*] Waiting for logs. To exit press CTRL+C')
        def callback(ch, method, properties, body):
            obj = json.loads(body)
            print(f" [x] {obj}")
            if util.verificar_assinatura(obj["Data"], obj["Signature"], "chave_publica"):
                print(f" [x] Assinatura valida!")
            else:
                print(f" [x] Assinatura inválida!")

if __name__ == "__main__":
    Ranking = Ranking()
    thread_receive = threading.Thread(target=Ranking.receive_voto)
    thread_receive.start()
