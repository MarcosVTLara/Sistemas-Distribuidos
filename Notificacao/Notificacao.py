import pika
import json
import Util.util as util
import threading

class Notificacao:
    def __init__(self):
        self.connection_1 = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.connection_2 = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel_1 = self.connection_1.channel()
        self.channel_1.exchange_declare(exchange='Promocoes', exchange_type='direct')
        self.channel_2 = self.connection_2.channel()
        self.channel_2.exchange_declare(exchange='Promocoes', exchange_type='direct')
        self.ranking = {}
        self.hot_deal_value = 5
        self.lista_promocoes = []

    def receive_publicada(self):
        result = self.channel_1.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel_1.queue_bind(exchange='Promocoes', queue=queue_name,routing_key="publicada")
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
        self.channel_2.queue_bind(exchange='Promocoes', queue=queue_name, routing_key="destaque")
        print(' [*] Waiting for logs. To exit press CTRL+C')
        def callback(ch, method, properties, body):
            obj = json.loads(body)
            print(f" [x] {obj}")
            if util.verificar_assinatura(obj["Data"], obj["Signature"], r".\publicas\Ranking_public.pem"):
                print(f" [x] Assinatura valida!")
                categoria = self.verifica_categoria(obj["Data"]["promocao"])
                self.enviar_categoria(f"hot deal {obj['Data']['promocao']}", categoria)

            else:
                print(f" [x] Assinatura inválida!")

        self.channel_2.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel_2.start_consuming()

    def verifica_categoria(self, promocao):
        for promocao_lista in self.lista_promocoes:
            if promocao_lista["promocao"] == promocao:
                return promocao_lista["categoria"]
        return None
    
    def enviar_categoria(self, promocao, categoria):
        dados = { 
            "promocao": promocao,
        }
        message = {
            "Signature": util.gerar_assinatura(dados, r".\privadas\Notificacao_private.pem"),
            "Data": dados
        }
        body = json.dumps(message).encode('utf-8')
        match categoria:
            case "Eletrônicos":
                self.channel_2.basic_publish(exchange='Promocoes', routing_key="eletronicos", body=body)
                print(f" [x] Sent {message} - Eletrônicos")
            case "Roupas":
                self.channel_2.basic_publish(exchange='Promocoes', routing_key="roupas", body=body)
                print(f" [x] Sent {message} - Roupas")
            case "Alimentos":
                self.channel_2.basic_publish(exchange='Promocoes', routing_key="alimentos", body=body)
                print(f" [x] Sent {message} - Alimentos")
    
    def close(self):
        self.connection_1.close()
        self.connection_2.close()

if __name__ == "__main__":
    Notificacao = Notificacao()
    thread_receive_publicada = threading.Thread(target=Notificacao.receive_publicada)
    thread_receive_publicada.start()
    thread_receive_destaque = threading.Thread(target=Notificacao.receive_destaque)
    thread_receive_destaque.start()
