import React from 'react';
import { Page, Title, List, Card, Tag, Message, Time, Empty } from './Feed.styles';

const mockNotificacoes = [
    { id: 1, categoria: 'Eletrônicos', mensagem: 'Nova promoção: TV 55" com 30% off', hora: '14:32' },
    { id: 2, categoria: 'Moda',        mensagem: 'Liquidação de inverno – até 50%',   hora: '13:10' },
    { id: 3, categoria: 'Alimentos',   mensagem: 'Frete grátis acima de R$80',         hora: '11:55' },
];

function Feed() {
    const notificacoes = mockNotificacoes;

    return (
        <Page>
            <Title>Feed de Notificações</Title>
            {notificacoes.length === 0
                ? <Empty>Nenhuma notificação no momento.</Empty>
                : (
                    <List>
                        {notificacoes.map(n => (
                            <Card key={n.id}>
                                <Tag>{n.categoria}</Tag>
                                <Message>{n.mensagem}</Message>
                                <Time>{n.hora}</Time>
                            </Card>
                        ))}
                    </List>
                )
            }
        </Page>
    );
}

export default Feed;
