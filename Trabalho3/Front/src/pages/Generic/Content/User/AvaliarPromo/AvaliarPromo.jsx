import React, { useEffect, useState } from 'react';
import { Page, Title, List, Card, Tag, Nome, Desc, Buttons, BtnPos, BtnNeg, Votos } from './AvaliarPromo.styles';
import { listarPromocoes, votar } from 'src/Fetch/FetchData';

function AvaliarPromo() {
    const [promos, setPromos] = useState([]);
    const [erro, setErro] = useState('');

    const carregar = async () => {
        try {
            setPromos(await listarPromocoes());
            setErro('');
        } catch (e) {
            setErro(e.message);
        }
    };

    useEffect(() => { carregar(); }, []);

    const handleVotar = async (id, voto) => {
        try {
            const { promocao } = await votar(id, voto);
            setPromos(prev => prev.map(p => (p.id === promocao.id ? promocao : p)));
        } catch (e) {
            setErro(e.message);
        }
    };

    return (
        <Page>
            <Title>Votar em Promoções</Title>
            {erro && <Desc style={{ color: '#e53e3e' }}>{erro}</Desc>}
            {promos.length === 0 && !erro && <Desc>Nenhuma promoção disponível ainda.</Desc>}
            <List>
                {promos.map(p => (
                    <Card key={p.id}>
                        <Tag>{p.categoria}</Tag>
                        <Nome>{p.nome}</Nome>
                        <Desc>{p.descricao}</Desc>
                        <Buttons>
                            <BtnPos onClick={() => handleVotar(p.id, 'Positivo')}>👍 Positivo</BtnPos>
                            <BtnNeg onClick={() => handleVotar(p.id, 'Negativo')}>👎 Negativo</BtnNeg>
                        </Buttons>
                        <Votos>+{p.votos.pos} positivos &nbsp;·&nbsp; -{p.votos.neg} negativos</Votos>
                    </Card>
                ))}
            </List>
        </Page>
    );
}

export default AvaliarPromo;
