import React, { useEffect, useState } from 'react';
import { Page, Title, List, Card, Tag, Nome, Desc, Votos, Empty } from './ConsultarPromo.styles';
import { listarPromocoesPublicadas } from 'src/Fetch/FetchData';

function ConsultarPromo() {
    const [promos, setPromos] = useState([]);
    const [erro, setErro] = useState('');

    const carregar = async () => {
        try {
            setPromos(await listarPromocoesPublicadas());
            setErro('');
        } catch (e) {
            setErro(e.message);
        }
    };

    useEffect(() => { carregar(); }, []);

    return (
        <Page>
            <Title>Consultar Promoções Publicadas</Title>
            {erro && <Desc style={{ color: '#e53e3e' }}>{erro}</Desc>}
            {promos.length === 0 && !erro
                ? <Empty>Nenhuma promoção publicada no momento.</Empty>
                : (
                    <List>
                        {promos.map(p => (
                            <Card key={p.id}>
                                <Tag>{p.categoria}</Tag>
                                <Nome>{p.nome}</Nome>
                                <Desc>{p.descricao}</Desc>
                                <Votos>+{p.votos.pos} positivos &nbsp;·&nbsp; -{p.votos.neg} negativos</Votos>
                            </Card>
                        ))}
                    </List>
                )
            }
        </Page>
    );
}

export default ConsultarPromo;
