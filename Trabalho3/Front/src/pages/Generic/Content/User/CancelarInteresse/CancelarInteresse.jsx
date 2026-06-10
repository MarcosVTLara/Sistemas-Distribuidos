import React, { useState } from 'react';
import { Page, Title, List, Row, Info, Nome, Sub, BtnRemove, Empty } from './CancelarInteresse.styles';
import GlobalVariablesConsumer from 'src/context/GlobalVariables';
import { cancelarInteresse } from 'src/Fetch/FetchData';

function CancelarInteresse() {
    const { sessao, interesses, setInteresses } = GlobalVariablesConsumer();
    const [erro, setErro] = useState('');

    const handleRemove = async (categoria) => {
        try {
            const { interesses: atualizados } = await cancelarInteresse(sessao, categoria);
            setInteresses(atualizados);
            setErro('');
        } catch (e) {
            setErro(e.message);
        }
    };

    return (
        <Page>
            <Title>Cancelar Interesse</Title>
            {erro && <Sub style={{ color: '#e53e3e' }}>{erro}</Sub>}
            {interesses.length === 0
                ? <Empty>Você não possui interesses registrados.</Empty>
                : (
                    <List>
                        {interesses.map(c => (
                            <Row key={c}>
                                <Info>
                                    <Nome>{c}</Nome>
                                    <Sub>Interesse registrado</Sub>
                                </Info>
                                <BtnRemove onClick={() => handleRemove(c)}>– Remover</BtnRemove>
                            </Row>
                        ))}
                    </List>
                )
            }
        </Page>
    );
}

export default CancelarInteresse;
