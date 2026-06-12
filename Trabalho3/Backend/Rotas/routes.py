"""Camada de entrada HTTP (REST + SSE) que expõe o Gateway para o frontend.

Aqui ficam apenas os endpoints Flask. As rotas de promoção/voto falam com
`gateway`; as rotas de interesse/stream falam com `gateway.sse`
(o GerenciadorSSE). Nenhuma lógica de negócio ou de mensageria mora aqui.
"""
from flask import Flask, request, jsonify, Response, stream_with_context

CATEGORIAS = ["Eletrônicos", "Roupas", "Alimentos"]


def build_app(gateway):
    app = Flask(__name__)

    @app.after_request
    def cors(resp):
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return resp

    @app.route("/promocoes", methods=["POST", "GET"])
    def promocoes():
        if request.method == "GET":
            apenas_publicadas = request.args.get("publicadas") in ("1", "true", "True")
            return jsonify({"promocoes": gateway.listar_promocoes_api(apenas_publicadas)})
        body = request.get_json(silent=True) or {}
        nome = (body.get("nome") or "").strip()
        descricao = (body.get("descricao") or "").strip()
        categoria = body.get("categoria")
        email = (body.get("email") or "").strip()
        assinatura = body.get("assinatura")
        if not nome or not descricao or categoria not in CATEGORIAS:
            return jsonify({"erro": "nome, descricao e categoria válida são obrigatórios"}), 400
        if not assinatura:
            return jsonify({"erro": "assinatura da loja é obrigatória"}), 400
        registro = gateway.cadastrar_promocao_api(nome, descricao, categoria, assinatura, email)
        if registro is None:
            return jsonify({"erro": "assinatura da loja inválida"}), 401
        return jsonify({"status": "promocao.recebida", "promocao": registro}), 202

    @app.route("/promocoes/<int:promo_id>/votar", methods=["POST"])
    def votar(promo_id):
        body = request.get_json(silent=True) or {}
        voto = body.get("voto")
        if voto not in ("Positivo", "Negativo"):
            return jsonify({"erro": "voto deve ser 'Positivo' ou 'Negativo'"}), 400
        registro = gateway.votar_api(promo_id, voto)
        if registro is None:
            return jsonify({"erro": "promoção não encontrada"}), 404
        return jsonify({"status": "promocao.voto", "promocao": registro})

    @app.route("/interesses", methods=["POST", "GET"])
    def interesses():
        if request.method == "GET":
            sessao = request.args.get("sessao", "")
            return jsonify({"interesses": gateway.sse.interesses_da_sessao(sessao)})
        body = request.get_json(silent=True) or {}
        sessao = body.get("sessao")
        categoria = body.get("categoria")
        if not sessao or categoria not in CATEGORIAS:
            return jsonify({"erro": "sessao e categoria válida são obrigatórios"}), 400
        gateway.sse.registrar_interesse(sessao, categoria)
        return jsonify({"status": "interesse registrado", "interesses": gateway.sse.interesses_da_sessao(sessao)})

    @app.route("/interesses/<categoria>", methods=["DELETE"])
    def cancelar_interesse(categoria):
        sessao = request.args.get("sessao", "")
        if not sessao:
            return jsonify({"erro": "sessao é obrigatória"}), 400
        gateway.sse.cancelar_interesse(sessao, categoria)
        return jsonify({"status": "interesse cancelado", "interesses": gateway.sse.interesses_da_sessao(sessao)})

    @app.route("/sse")
    def sse():
        sessao = request.args.get("sessao", "")
        if not sessao:
            return jsonify({"erro": "sessao é obrigatória"}), 400
        resp = Response(stream_with_context(gateway.sse.stream_sse(sessao)), content_type="text/event-stream")
        resp.headers["Cache-Control"] = "no-cache"
        resp.headers["X-Accel-Buffering"] = "no"
        resp.headers["Connection"] = "keep-alive"
        return resp

    return app
