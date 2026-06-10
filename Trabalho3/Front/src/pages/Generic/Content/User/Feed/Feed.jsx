import React from 'react';
import { Page, Title, List, Card, Tag, Message, Time, Empty } from './Feed.styles';
import { subscribeFeed, getFeedSnapshot } from 'src/Fetch/FetchData';

function Feed() {
    // Lê o feed do store externo: atualiza em tempo real a cada evento SSE,
    // sem precisar sair e voltar para a página.
    const feed = React.useSyncExternalStore(subscribeFeed, getFeedSnapshot);

    return (
        <Page>
            <Title>Feed de Notificações</Title>
            {feed.length === 0
                ? <Empty>Nenhuma notificação no momento. Registre interesses para receber promoções.</Empty>
                : (
                    <List>
                        {feed.map(n => (
                            <Card key={n.key}>
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
