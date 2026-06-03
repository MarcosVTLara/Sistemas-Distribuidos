import React from 'react';
import { Page, Title, List, Row, Info, Nome, Sub, BtnRemove, Empty } from './CancelarInteresse.styles';

const mockInteresses = [
    { id: 1, nome: 'Eletrônicos', promos: 8 },
    { id: 2, nome: 'Alimentos',   promos: 12 },
];

function CancelarInteresse() {
    return (
        <Page>
            <Title>Cancelar Interesse</Title>
            {mockInteresses.length === 0
                ? <Empty>Você não possui interesses registrados.</Empty>
                : (
                    <List>
                        {mockInteresses.map(c => (
                            <Row key={c.id}>
                                <Info>
                                    <Nome>{c.nome}</Nome>
                                    <Sub>{c.promos} promoções ativas</Sub>
                                </Info>
                                <BtnRemove>– Remover</BtnRemove>
                            </Row>
                        ))}
                    </List>
                )
            }
        </Page>
    );
}

export default CancelarInteresse;
