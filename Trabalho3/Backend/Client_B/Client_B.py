#!/usr/bin/env python
import pika
import json
import threading

# Categorias de interesse hardcoded conforme o trabalho
CATEGORIAS_INTERESSE = ["promocao.eletronicos"]

class Client_B:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='Promocoes', exchange_type='topic')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        for routing_key in CATEGORIAS_INTERESSE:
            self.channel.queue_bind(
                exchange='Promocoes', queue=self.queue_name, routing_key=routing_key)
            print(f" [*] Inscrito em: {routing_key}")

    def receive(self):
        print(' [*] Aguardando notificações de promoções. Para sair pressione CTRL+C')
        def callback(ch, method, properties, body):
            dados = json.loads(body)
            print(f"\n [!] NOVA NOTIFICAÇÃO [{method.routing_key}]: {dados['promocao']}")
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    client = Client_B()
    thread_receive = threading.Thread(target=client.receive)
    thread_receive.start()
