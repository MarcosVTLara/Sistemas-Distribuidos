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
        self.lista_destaques = []

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
                self.lista_promocoes.append(obj["Data"])
                self.enviar_publicada(self.lista_promocoes)
            else:
                print(f" [x] Assinatura inválida!")
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def enviar_publicada(self, lista_promocoes):
        dados = { 
            "Data":{
                "destaque": lista_promocoes,
            }
        }
        message = {
            "Signature": util.gerar_assinatura(dados, "chave_privada"),
            "Data":{
                "destaque": lista_promocoes,
            }
        }
        body = json.dumps(message).encode('utf-8')
        self.channel.basic_publish(exchange='Promocoes', routing_key="publicada", body=body)
        print(f" [x] Sent {message}")

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    Ranking = Ranking()
    thread_receive = threading.Thread(target=Ranking.receive_recebida)
    thread_receive.start()
