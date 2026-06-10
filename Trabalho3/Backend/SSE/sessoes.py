"""Gerência de sessões e streaming SSE (Server-Sent Events).

Cada sessão (identificada por um id vindo do frontend) guarda:
  - as categorias de interesse do usuário;
  - as filas dos clientes conectados via SSE.

O Gateway usa `broadcast()` para empurrar eventos; as rotas usam
`stream_sse()` para manter a conexão aberta com o navegador.
"""
import json
import queue
import threading


class GerenciadorSSE:
    def __init__(self):
        self.sessoes = {}
        self.sessoes_lock = threading.Lock()

    def _get_sessao_locked(self, sessao):
        if sessao not in self.sessoes:
            self.sessoes[sessao] = {"clientes": set(), "interesses": set()}
        return self.sessoes[sessao]

    # ------------------------------------------------------------------ #
    # Interesses por categoria
    # ------------------------------------------------------------------ #
    def registrar_interesse(self, sessao, categoria):
        with self.sessoes_lock:
            self._get_sessao_locked(sessao)["interesses"].add(categoria)

    def cancelar_interesse(self, sessao, categoria):
        with self.sessoes_lock:
            self._get_sessao_locked(sessao)["interesses"].discard(categoria)

    def interesses_da_sessao(self, sessao):
        with self.sessoes_lock:
            return sorted(self._get_sessao_locked(sessao)["interesses"])

    # ------------------------------------------------------------------ #
    # Clientes SSE conectados
    # ------------------------------------------------------------------ #
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

    def broadcast(self, tipo, data, categoria=None):
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
