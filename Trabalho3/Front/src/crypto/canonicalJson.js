function escapeString(str) {
    let out = '"';
    for (const ch of str) {            
        const cp = ch.codePointAt(0);
        switch (ch) {
            case '"':  out += '\\"';  continue;
            case '\\': out += '\\\\'; continue;
            case '\b': out += '\\b';  continue;
            case '\f': out += '\\f';  continue;
            case '\n': out += '\\n';  continue;
            case '\r': out += '\\r';  continue;
            case '\t': out += '\\t';  continue;
        }
        if (cp >= 0x20 && cp <= 0x7e) {
            out += ch;
        } else if (cp > 0xffff) {

            const v = cp - 0x10000;
            const hi = 0xd800 + (v >> 10);
            const lo = 0xdc00 + (v & 0x3ff);
            out += '\\u' + hi.toString(16).padStart(4, '0');
            out += '\\u' + lo.toString(16).padStart(4, '0');
        } else {
            out += '\\u' + cp.toString(16).padStart(4, '0');
        }
    }
    return out + '"';
}

function numberToJson(n) {
    if (!Number.isFinite(n)) {
        throw new Error(`Número não serializável em JSON canônico: ${n}`);
    }
    return String(n);
}

export function canonicalize(value) {
    if (value === null) return 'null';
    const t = typeof value;
    if (t === 'boolean') return value ? 'true' : 'false';
    if (t === 'number') return numberToJson(value);
    if (t === 'string') return escapeString(value);
    if (Array.isArray(value)) {
        return '[' + value.map(canonicalize).join(',') + ']';
    }
    if (t === 'object') {
        const keys = Object.keys(value).sort();
        const partes = keys.map((k) => escapeString(k) + ':' + canonicalize(value[k]));
        return '{' + partes.join(',') + '}';
    }
    throw new Error(`Tipo não serializável em JSON canônico: ${t}`);
}

export { escapeString };
