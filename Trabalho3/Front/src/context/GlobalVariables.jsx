import React from 'react';
import userTypes from 'src/constants/userTypes.json'
import { API_BASE, abrirSSE, pushFeed } from 'src/Fetch/FetchData';
const globalVariablesContext = React.createContext();

function getSessao() {
    let s = localStorage.getItem('sessao');
    if (!s) {
        s = (crypto.randomUUID && crypto.randomUUID()) || String(Date.now() + Math.random());
        localStorage.setItem('sessao', s);
    }
    return s;
}

function useGlobalVariables(){
    const [login, setLogin] = React.useState(userTypes[0])
    const [menu, setMenu] = React.useState(userTypes[0])
    const [sessao] = React.useState(getSessao)
    const [interesses, setInteresses] = React.useState([])
    const [lojaEmail, setLojaEmail] = React.useState(() => localStorage.getItem('lojaEmail') || '')

    // Sincroniza os interesses registrados no backend ao iniciar a sessão.
    React.useEffect(() => {
        fetch(`${API_BASE}/interesses?sessao=${encodeURIComponent(sessao)}`)
            .then(r => r.json())
            .then(data => setInteresses(data.interesses || []))
            .catch(() => {});
    }, [sessao]);

    // Abre a conexão SSE com o Gateway uma única vez por sessão e empurra os
    // eventos para o store externo do feed (lido pelo componente Feed).
    React.useEffect(() => {
        const source = abrirSSE(sessao, ({ tipo, data }) => {
            const hora = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
            const mensagem = tipo === 'hotdeal'
                ? `🔥 HOT DEAL: ${data.nome}`
                : `Nova promoção: ${data.nome}${data.descricao ? ' — ' + data.descricao : ''}`;
            pushFeed({ categoria: data.categoria, mensagem, hora, tipo });
        });
        return () => source.close();
    }, [sessao]);

    return{
        login,
        menu,
        sessao,
        interesses,
        lojaEmail,

        setInteresses,

        salvarLojaEmail(email){
            localStorage.setItem('lojaEmail', email);
            setLojaEmail(email);
        },

        newLogin(newUser){
            return new Promise((resolve) => {
                setLogin(newUser);
                resolve();
            })
        },

        newMenu(newUser){
            return new Promise((resolve) => {
                setMenu(newUser);
                resolve();
            })
        }
    };
}
export function GlobalVariablesProvider({ children }){
    const auth = useGlobalVariables();
    return(
        <globalVariablesContext.Provider value={auth}>
            {children}
        </globalVariablesContext.Provider>
    );
}

export default function GlobalVariavblesConsumer(){
    return React.useContext(globalVariablesContext);
}
