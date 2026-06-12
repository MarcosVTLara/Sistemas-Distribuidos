import { assinarPromocao } from '../src/crypto/signPromocao.js';

const arg = process.argv[2] || '{}';
const campos = JSON.parse(arg);
const { canonico, assinatura } = assinarPromocao(campos);
process.stdout.write(JSON.stringify({ canonico, assinatura }));
