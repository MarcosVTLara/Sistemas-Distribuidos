#!/usr/bin/env python
import pika
import sys
import json
import Util.util as util
import threading
import questionary


class Getway:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='Promocoes', exchange_type='direct')
        self.lista_promocoes = []

    def receive_publicada(self):
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange='Promocoes', queue=queue_name, routing_key="publicada")
        print(' [*] Waiting for logs. To exit press CTRL+C')
        def callback(ch, method, properties, body):
            obj = json.loads(body)
            print(f" [x] {obj}")
            if util.verificar_assinatura(obj["Data"], obj["Signature"], r".\publicas\Promocao_public.pem"):
                print(f" [x] Assinatura valida!")
                self.lista_promocoes.append(obj["Data"]["promocao"])
            else:
                print(f" [x] Assinatura inválida!")
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def enviar_promocao(self, promocao, categoria):
        dados = { 
            "promocao": promocao,
            "categoria": categoria,
        }
        message = {
            "Signature": util.gerar_assinatura(dados, r".\privadas\Getway_private.pem"),
            "Data": dados
        }

        body = json.dumps(message).encode('utf-8')
        self.channel.basic_publish(exchange='Promocoes', routing_key="recebida", body=body)
        print(f" [x] Sent {message}")

    def enviar_voto(self, voto, promocao):
        dados = { 
            "voto": voto,
            "promocao": promocao
        }
        message = {
            "Signature": util.gerar_assinatura(dados, r".\privadas\Getway_private.pem"),
            "Data": dados
        }
        body = json.dumps(message).encode('utf-8')
        self.channel.basic_publish(exchange='Promocoes', routing_key="voto", body=body)
        print(f" [x] Sent {message}")

    def start_ui(self):
        while True:
            Choice = questionary.select("Selecione a ação", choices=["Cadastrar Promoção", "Listar Promoções", "Votar em Promoção", "Exit"]).ask()
            match Choice:
                case "Cadastrar Promoção":
                    self.cadastrar_promocao()
                
                case"Listar Promoções":
                    self.listar_promocoes()

                case "Votar em Promoção":
                    self.votar_em_promocao()
                case "Exit":
                    self.connection.close()
                    break

    def cadastrar_promocao(self):
        answers = questionary.form(
        promocao = questionary.text("Digite a promoção:"),
        categoria = questionary.select("Selecione a categoria", choices=["Eletrônicos", "Roupas", "Alimentos"])
        ).ask()
        self.enviar_promocao(answers["promocao"], answers["categoria"])

    def listar_promocoes(self):
        if len(self.lista_promocoes) == 0:
            print("Nenhuma promoção disponível.")
            return
        print("Promoções disponíveis:")
        for promocao in self.lista_promocoes:
            print(f"- {promocao}")

    def votar_em_promocao(self):
        if len(self.lista_promocoes) == 0:
            print("Nenhuma promoção disponível para votar.")
            return

        choices = []
        for promocao in self.lista_promocoes:
            choices.append(promocao["promocao"])

        promocao_escolhida = questionary.select(
            "Selecione a promoção para votar",
            choices=choices
        ).ask()
        
        valor = questionary.select("Valor do voto", choices=["Positivo", "Negativo"]).ask()

        self.enviar_voto(valor, promocao_escolhida)


if __name__ == "__main__":
    getway = Getway()
    thread_receive = threading.Thread(target=getway.receive_publicada)
    thread_receive.start()
    getway.start_ui()