import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { canonicalize } from './canonicalJson.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CHAVE_PRIVADA_LOJA = path.resolve(
    __dirname, '..', '..', '..', 'Backend', 'privadas', 'loja_private.pem'
);


export function montarDadosLoja({ nome, descricao, categoria, email }) {
    return {
        promocao: nome,
        descricao: descricao,
        categoria: categoria,
        email: email,
    };
}

export function assinarPromocao(campos, caminhoChave = CHAVE_PRIVADA_LOJA) {
    const dados = montarDadosLoja(campos);
    const canonico = canonicalize(dados);

    const privateKey = crypto.createPrivateKey({
        key: fs.readFileSync(caminhoChave),
        format: 'pem',
    });

    const assinatura = crypto.sign('sha256', Buffer.from(canonico, 'utf8'), {
        key: privateKey,
        padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
        saltLength: crypto.constants.RSA_PSS_SALTLEN_MAX_SIGN,
    });

    return { canonico, assinatura: assinatura.toString('hex') };
}

export { CHAVE_PRIVADA_LOJA };
