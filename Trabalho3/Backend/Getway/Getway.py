#!/usr/bin/env python
import pika
import os
import json
import queue
import Util.util as util
import threading
import questionary
from flask import Flask, request, jsonify, Response, stream_with_context

util.carregar_env()

RABBIT_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
API_PORT = int(os.environ.get("GATEWAY_PORT", "8000"))

# Categorias suportadas -> usadas para validação e roteamento por interesse
CATEGORIAS = ["Eletrônicos", "Roupas", "Alimentos"]


# O Gateway agora é uma API: expõe REST + SSE para o frontend e mantém a
# comunicação com os microsserviços via RabbitMQ (publish/consume).
class Getway:
    def __init__(self):
        params = pika.ConnectionParameters(host=RABBIT_HOST, heartbeat=0)
        self.connection_sub = pika.BlockingConnection(params)
        self.connection_pub = pika.BlockingConnection(params)
        self.channel_sub = self.connection_sub.channel()
        self.channel_sub.exchange_declare(exchange='Promocoes', exchange_type='topic')
        self.channel_pub = self.connection_pub.channel()
        self.channel_pub.exchange_declare(exchange='Promocoes', exchange_type='topic')
        self.pub_lock = threading.Lock()

        # Estado das promoções (mapa id -> promoção) e índice por nome
        self.lista_promocoes = []          # mantido por compatibilidade com a CLI
        self.promocoes = {}                # id -> {id, nome, descricao, categoria, votos}
        self.nome_para_id = {}             # nome -> id
        self.proximo_id = 1
        self.estado_lock = threading.Lock()

        # Sessões SSE: sessao -> {"clientes": set(Queue), "interesses": set(categorias)}
        self.sessoes = {}
        self.sessoes_lock = threading.Lock()
        self.hot_deals_enviados = set()

    # ------------------------------------------------------------------ #
    # Consumo do RabbitMQ -> repassa para os clientes SSE interessados
    # ------------------------------------------------------------------ #
    def receive_eventos(self):
        result = self.channel_sub.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        routing_keys = [
            "promocao.publicada",
            "promocao.destaque",
            "promocao.categoria",
            "notificacao.hotdeal",
        ]
        for routing_key in routing_keys:
            self.channel_sub.queue_bind(exchange='Promocoes', queue=queue_name, routing_key=routing_key)
        print(f" [*] Gateway aguardando eventos ({', '.join(routing_keys)}). CTRL+C para sair")

        def callback(ch, method, properties, body):
            try:
                obj = json.loads(body)
                if method.routing_key == "promocao.publicada":
                    self._on_publicada(obj)
                elif method.routing_key == "promocao.destaque":
                    self._on_destaque(obj)
                elif method.routing_key == "promocao.categoria":
                    self._on_categoria(obj)
                elif method.routing_key == "notificacao.hotdeal":
                    self._on_hotdeal(obj)
            except Exception as exc:
                print(f" [!] Erro ao processar {method.routing_key}; consumer SSE mantido ativo: {exc}")

        self.channel_sub.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel_sub.start_consuming()

    def _on_publicada(self, obj):
        if not util.verificar_assinatura(obj["Data"], obj["Signature"], r".\publicas\Promocao_public.pem"):
            print(" [x] promocao.publicada com assinatura inválida!")
            return
        promo = obj["Data"]["promocao"]
        registro = self._registrar_promocao(promo)
        print(f" [x] Promoção publicada: {registro}")
        self._broadcast("promocao", registro, categoria=registro["categoria"])

    def _on_hotdeal(self, obj):
        if not util.verificar_assinatura(obj["Data"], obj["Signature"], r".\publicas\Notificacao_public.pem"):
            print(" [x] notificacao.hotdeal com assinatura inválida!")
            return
        dados = obj["Data"]
        nome = dados.get("promocao")
        categoria = dados.get("categoria")
        evento = self._montar_evento_promocao(nome, categoria, dados.get("descricao", ""))
        print(f" [x] HOT DEAL recebido: {evento}")
        self._broadcast_hotdeal(evento)

    def _on_destaque(self, obj):
        if not util.verificar_assinatura(obj["Data"], obj["Signature"], r".\publicas\Ranking_public.pem"):
            print(" [x] promocao.destaque com assinatura inválida!")
            return
        nome = obj["Data"].get("promocao")
        evento = self._montar_evento_promocao(nome)
        print(f" [x] Destaque recebido: {evento}")
        self._broadcast_hotdeal(evento)

    def _on_categoria(self, obj):
        dados = obj.get("Data", obj)
        nome = dados.get("promocao")
        categoria = dados.get("categoria")
        evento = self._montar_evento_promocao(nome, categoria, dados.get("descricao", ""))
        if not evento["categoria"]:
            print(f" [!] promocao.categoria sem categoria conhecida: {evento}")
            return
        print(f" [x] Promoção por categoria recebida: {evento}")
        self._broadcast("promocao", evento, categoria=evento["categoria"])

    def _montar_evento_promocao(self, nome, categoria=None, descricao=""):
        with self.estado_lock:
            pid = self.nome_para_id.get(nome)
            registro = self.promocoes.get(pid, {}) if pid else {}
        return {
            "id": registro.get("id"),
            "nome": nome,
            "descricao": registro.get("descricao", descricao),
            "categoria": categoria or registro.get("categoria"),
        }

    def _broadcast_hotdeal(self, evento):
        nome = evento.get("nome")
        if nome:
            with self.estado_lock:
                if nome in self.hot_deals_enviados:
                    return
                self.hot_deals_enviados.add(nome)
        # Hot deal é destaque global: vai para todas as sessões SSE conectadas,
        # independente das categorias de interesse registradas.
        self._broadcast("hotdeal", evento)

    def _registrar_promocao(self, promo):
        """Cria/atualiza o registro local de uma promoção a partir do payload."""
        nome = promo["promocao"]
        with self.estado_lock:
            pid = self.nome_para_id.get(nome)
            if pid is None:
                pid = promo.get("id") or self.proximo_id
                self.proximo_id = max(self.proximo_id, pid) + 1
                registro = {
                    "id": pid,
                    "nome": nome,
                    "descricao": promo.get("descricao", ""),
                    "categoria": promo.get("categoria"),
                    "votos": {"pos": 0, "neg": 0},
                    "publicada": True,
                }
                self.promocoes[pid] = registro
                self.nome_para_id[nome] = pid
                self.lista_promocoes.append(promo)
            else:
                registro = self.promocoes[pid]
                registro["descricao"] = promo.get("descricao", registro["descricao"])
                registro["categoria"] = promo.get("categoria", registro["categoria"])
                registro["publicada"] = True
            return dict(registro)

    # ------------------------------------------------------------------ #
    # Publicação no RabbitMQ
    # ------------------------------------------------------------------ #
    def enviar_promocao(self, promocao, categoria, descricao="", email="", id=None):
        dados = {
            "id": id,
            "promocao": promocao,
            "descricao": descricao,
            "categoria": categoria,
            "email": email,
        }
        message = {
            "Signature": util.gerar_assinatura(dados, r".\privadas\Getway_private.pem"),
            "Data": dados
        }
        body = json.dumps(message).encode('utf-8')
        with self.pub_lock:
            self.channel_pub.basic_publish(exchange='Promocoes', routing_key="promocao.recebida", body=body)
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
        with self.pub_lock:
            self.channel_pub.basic_publish(exchange='Promocoes', routing_key="promocao.voto", body=body)
        print(f" [x] Sent {message}")

    # ------------------------------------------------------------------ #
    # API REST (chamada pelas rotas Flask)
    # ------------------------------------------------------------------ #
    def cadastrar_promocao_api(self, nome, descricao, categoria, email=""):
        with self.estado_lock:
            pid = self.proximo_id
            self.proximo_id += 1
            registro = {
                "id": pid,
                "nome": nome,
                "descricao": descricao,
                "categoria": categoria,
                "votos": {"pos": 0, "neg": 0},
                "publicada": False,
            }
            self.promocoes[pid] = registro
            self.nome_para_id[nome] = pid
        self.enviar_promocao(nome, categoria, descricao=descricao, email=email, id=pid)
        return dict(registro)

    def listar_promocoes_api(self, apenas_publicadas=False):
        with self.estado_lock:
            promos = [dict(p) for p in self.promocoes.values()]
        if apenas_publicadas:
            promos = [p for p in promos if p.get("publicada")]
        return promos

    def votar_api(self, promo_id, voto):
        with self.estado_lock:
            registro = self.promocoes.get(promo_id)
            if registro is None:
                return None
            nome = registro["nome"]
            if voto == "Positivo":
                registro["votos"]["pos"] += 1
            elif voto == "Negativo":
                registro["votos"]["neg"] += 1
            resultado = dict(registro)
        self.enviar_voto(voto, nome)
        return resultado

    # ------------------------------------------------------------------ #
    # Gerência de sessões / SSE
    # ------------------------------------------------------------------ #
    def _get_sessao(self, sessao):
        with self.sessoes_lock:
            return self._get_sessao_locked(sessao)

    def _get_sessao_locked(self, sessao):
        if sessao not in self.sessoes:
            self.sessoes[sessao] = {"clientes": set(), "interesses": set()}
        return self.sessoes[sessao]

    def registrar_interesse(self, sessao, categoria):
        with self.sessoes_lock:
            self._get_sessao_locked(sessao)["interesses"].add(categoria)

    def cancelar_interesse(self, sessao, categoria):
        with self.sessoes_lock:
            self._get_sessao_locked(sessao)["interesses"].discard(categoria)

    def interesses_da_sessao(self, sessao):
        with self.sessoes_lock:
            return sorted(self._get_sessao_locked(sessao)["interesses"])

    def _adicionar_cliente_sse(self, sessao):
        fila = queue.Queue()
        with self.sessoes_lock:
            self._get_sessao_locked(sessao)["clientes"].add(fila)
        return fila

    def _remover_cliente_sse(self, sessao, fila):
        with self.sessoes_lock:
            dados_sessao = self.sessoes.get(sessao)
            if dados_sessao:
                dados_sessao["clientes"].discard(fila)

    def _broadcast(self, tipo, data, categoria=None):
        evento = {"event": tipo, "data": data}
        with self.sessoes_lock:
            sessoes = [
                {"interesses": set(s["interesses"]), "clientes": list(s["clientes"])}
                for s in self.sessoes.values()
            ]
        for s in sessoes:
            # Filtra por categorias de interesse registradas na sessão
            if categoria is not None and categoria not in s["interesses"]:
                continue
            for fila in s["clientes"]:
                fila.put(evento)

    def stream_sse(self, sessao):
        fila = self._adicionar_cliente_sse(sessao)
        try:
            yield ": conectado\n\n"
            while True:
                try:
                    evento = fila.get(timeout=15)
                    yield f"event: {evento['event']}\ndata: {json.dumps(evento['data'])}\n\n"
                except queue.Empty:
                    yield ": keep-alive\n\n"
        finally:
            self._remover_cliente_sse(sessao, fila)

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


# ---------------------------------------------------------------------- #
# Aplicação Flask (REST + SSE) que expõe o Gateway para o frontend
# ---------------------------------------------------------------------- #
def build_app(gateway):
    app = Flask(__name__)

    @app.after_request
    def cors(resp):
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return resp

    @app.route("/promocoes", methods=["OPTIONS", "POST", "GET"])
    def promocoes():
        if request.method == "OPTIONS":
            return ("", 204)
        if request.method == "GET":
            apenas_publicadas = request.args.get("publicadas") in ("1", "true", "True")
            return jsonify({"promocoes": gateway.listar_promocoes_api(apenas_publicadas)})
        body = request.get_json(silent=True) or {}
        nome = (body.get("nome") or "").strip()
        descricao = (body.get("descricao") or "").strip()
        categoria = body.get("categoria")
        email = (body.get("email") or "").strip()
        if not nome or not descricao or categoria not in CATEGORIAS:
            return jsonify({"erro": "nome, descricao e categoria válida são obrigatórios"}), 400
        registro = gateway.cadastrar_promocao_api(nome, descricao, categoria, email)
        return jsonify({"status": "promocao.recebida", "promocao": registro}), 202

    @app.route("/promocoes/<int:promo_id>/votar", methods=["OPTIONS", "POST"])
    def votar(promo_id):
        if request.method == "OPTIONS":
            return ("", 204)
        body = request.get_json(silent=True) or {}
        voto = body.get("voto")
        if voto not in ("Positivo", "Negativo"):
            return jsonify({"erro": "voto deve ser 'Positivo' ou 'Negativo'"}), 400
        registro = gateway.votar_api(promo_id, voto)
        if registro is None:
            return jsonify({"erro": "promoção não encontrada"}), 404
        return jsonify({"status": "promocao.voto", "promocao": registro})

    @app.route("/interesses", methods=["OPTIONS", "POST", "GET"])
    def interesses():
        if request.method == "OPTIONS":
            return ("", 204)
        if request.method == "GET":
            sessao = request.args.get("sessao", "")
            return jsonify({"interesses": gateway.interesses_da_sessao(sessao)})
        body = request.get_json(silent=True) or {}
        sessao = body.get("sessao")
        categoria = body.get("categoria")
        if not sessao or categoria not in CATEGORIAS:
            return jsonify({"erro": "sessao e categoria válida são obrigatórios"}), 400
        gateway.registrar_interesse(sessao, categoria)
        return jsonify({"status": "interesse registrado", "interesses": gateway.interesses_da_sessao(sessao)})

    @app.route("/interesses/<categoria>", methods=["OPTIONS", "DELETE"])
    def cancelar_interesse(categoria):
        if request.method == "OPTIONS":
            return ("", 204)
        sessao = request.args.get("sessao", "")
        if not sessao:
            return jsonify({"erro": "sessao é obrigatória"}), 400
        gateway.cancelar_interesse(sessao, categoria)
        return jsonify({"status": "interesse cancelado", "interesses": gateway.interesses_da_sessao(sessao)})

    @app.route("/sse")
    def sse():
        sessao = request.args.get("sessao", "")
        if not sessao:
            return jsonify({"erro": "sessao é obrigatória"}), 400
        resp = Response(stream_with_context(gateway.stream_sse(sessao)), content_type="text/event-stream")
        resp.headers["Cache-Control"] = "no-cache"
        resp.headers["X-Accel-Buffering"] = "no"
        resp.headers["Connection"] = "keep-alive"
        return resp

    return app


if __name__ == "__main__":
    getway = Getway()
    thread_receive = threading.Thread(target=getway.receive_eventos, daemon=True)
    thread_receive.start()
    app = build_app(getway)
    print(f" [*] Gateway REST + SSE em http://localhost:{API_PORT}")
    app.run(host="0.0.0.0", port=API_PORT, threaded=True, use_reloader=False)
