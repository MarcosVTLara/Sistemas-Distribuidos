export const API_BASE = 'http://localhost:8000';

async function asJson(resp) {
    const data = await resp.json().catch(() => ({}));
    if (!resp.ok) throw new Error(data.erro || `Erro ${resp.status}`);
    return data;
}

export async function listarPromocoes() {
    const resp = await fetch(`${API_BASE}/promocoes`);
    const data = await asJson(resp);
    return data.promocoes || [];
}

export async function listarPromocoesPublicadas() {
    const resp = await fetch(`${API_BASE}/promocoes?publicadas=1`);
    const data = await asJson(resp);
    return data.promocoes || [];
}

export async function cadastrarPromocao({ nome, descricao, categoria, email }) {
    const dados = {
        nome: (nome || '').trim(),
        descricao: (descricao || '').trim(),
        categoria,
        email: (email || '').trim(),
    };

    const assinResp = await fetch('/api/assinar-promocao', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados),
    });
    const { assinatura, erro } = await assinResp.json().catch(() => ({}));
    if (!assinResp.ok || !assinatura) {
        throw new Error(erro || 'Falha ao assinar a promoção');
    }

    const resp = await fetch(`${API_BASE}/promocoes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...dados, assinatura }),
    });
    return asJson(resp);
}

export async function votar(promoId, voto) {
    const resp = await fetch(`${API_BASE}/promocoes/${promoId}/votar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ voto }),
    });
    return asJson(resp);
}

export async function registrarInteresse(sessao, categoria) {
    const resp = await fetch(`${API_BASE}/interesses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessao, categoria }),
    });
    return asJson(resp);
}

export async function cancelarInteresse(sessao, categoria) {
    const resp = await fetch(
        `${API_BASE}/interesses/${encodeURIComponent(categoria)}?sessao=${encodeURIComponent(sessao)}`,
        { method: 'DELETE' }
    );
    return asJson(resp);
}


export function abrirSSE(sessao, onEvent) {
    const source = new EventSource(`${API_BASE}/sse?sessao=${encodeURIComponent(sessao)}`);
    source.addEventListener('promocao', (e) => onEvent({ tipo: 'promocao', data: JSON.parse(e.data) }));
    source.addEventListener('hotdeal', (e) => onEvent({ tipo: 'hotdeal', data: JSON.parse(e.data) }));
    source.onerror = (e) => {
        console.warn('Conexão SSE instável; o navegador tentará reconectar automaticamente.', e);
    };
    return source;
}

let feedState = [];
let feedSeq = 0;
const feedListeners = new Set();

export function subscribeFeed(listener) {
    feedListeners.add(listener);
    return () => feedListeners.delete(listener);
}

export function getFeedSnapshot() {
    return feedState;
}

export function pushFeed(item) {
    // Chave SEMPRE única (contador monotônico), mesmo que dois eventos cheguem
    // no mesmo milissegundo ou duplicados — evita colisão de key no React,
    // que quebrava a lista do Feed.
    feedSeq += 1;
    feedState = [{ ...item, key: feedSeq }, ...feedState];
    feedListeners.forEach((l) => l());
}

export default {
    API_BASE, listarPromocoes, listarPromocoesPublicadas, cadastrarPromocao, votar,
    registrarInteresse, cancelarInteresse, abrirSSE,
    subscribeFeed, getFeedSnapshot, pushFeed,
};
