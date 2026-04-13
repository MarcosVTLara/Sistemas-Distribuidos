#!/usr/bin/env python
import pika
import json
import Util.util as util
import threading

class Promocao:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='Promocoes', exchange_type='topic')

    def receive_recebida(self):
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange='Promocoes', queue=queue_name, routing_key="promocao.recebida")
        print(' [*] Waiting for logs. To exit press CTRL+C')
        def callback(ch, method, properties, body):
            obj = json.loads(body)
            print(f" [x] {obj}")
            if util.verificar_assinatura(obj["Data"], obj["Signature"], r".\publicas\Getway_public.pem"):
                print(f" [x] Assinatura valida!")
                self.enviar_publicada(obj["Data"])
            else:
                print(f" [x] Assinatura inválida!")
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def enviar_publicada(self, promocao):
        dados = { 
            "promocao": promocao,
        }
        message = {
            "Signature": util.gerar_assinatura(dados, r".\privadas\Promocao_private.pem"),
            "Data": dados
        }
        body = json.dumps(message).encode('utf-8')
        self.channel.basic_publish(exchange='Promocoes', routing_key="promocao.publicada", body=body)
        print(f" [x] Sent {message}")


    def close(self):
        self.connection.close()

if __name__ == "__main__":
    Promocao = Promocao()
    thread_receive = threading.Thread(target=Promocao.receive_recebida)
    thread_receive.start()
