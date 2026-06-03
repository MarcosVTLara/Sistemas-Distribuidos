import React from 'react';
import { Page, Title, List, Row, Info, Nome, Sub, BtnAdd } from './RegistrarInteresse.styles';

const mockCategorias = [
    { id: 1, nome: 'Eletrônicos', promos: 8 },
    { id: 2, nome: 'Moda',        promos: 5 },
    { id: 3, nome: 'Alimentos',   promos: 12 },
    { id: 4, nome: 'Esportes',    promos: 3 },
];

function RegistrarInteresse() {
    return (
        <Page>
            <Title>Registrar Interesse</Title>
            <List>
                {mockCategorias.map(c => (
                    <Row key={c.id}>
                        <Info>
                            <Nome>{c.nome}</Nome>
                            <Sub>{c.promos} promoções ativas</Sub>
                        </Info>
                        <BtnAdd>+ Adicionar</BtnAdd>
                    </Row>
                ))}
            </List>
        </Page>
    );
}

export default RegistrarInteresse;
