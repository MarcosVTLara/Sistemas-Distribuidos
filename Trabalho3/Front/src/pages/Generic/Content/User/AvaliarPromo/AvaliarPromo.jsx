import React from 'react';
import { Page, Title, List, Card, Tag, Nome, Desc, Buttons, BtnPos, BtnNeg, Votos } from './AvaliarPromo.styles';

const mockPromos = [
    { id: 1, nome: 'TV 55" Samsung', categoria: 'Eletrônicos', descricao: '30% de desconto até domingo', votos: { pos: 24, neg: 3 } },
    { id: 2, nome: 'Tênis Nike Air',  categoria: 'Moda',        descricao: 'Compre 2 leve 3 em toda linha',  votos: { pos: 12, neg: 7 } },
    { id: 3, nome: 'Kit Churrasco',   categoria: 'Alimentos',   descricao: 'Frete grátis + brinde',          votos: { pos: 31, neg: 1 } },
];

function AvaliarPromo() {
    return (
        <Page>
            <Title>Votar em Promoções</Title>
            <List>
                {mockPromos.map(p => (
                    <Card key={p.id}>
                        <Tag>{p.categoria}</Tag>
                        <Nome>{p.nome}</Nome>
                        <Desc>{p.descricao}</Desc>
                        <Buttons>
                            <BtnPos>👍 Positivo</BtnPos>
                            <BtnNeg>👎 Negativo</BtnNeg>
                        </Buttons>
                        <Votos>+{p.votos.pos} positivos &nbsp;·&nbsp; -{p.votos.neg} negativos</Votos>
                    </Card>
                ))}
            </List>
        </Page>
    );
}

export default AvaliarPromo;
