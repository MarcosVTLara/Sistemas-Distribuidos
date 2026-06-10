import React, { useState } from 'react';
import { Page, Title, List, Row, Info, Nome, Sub, BtnAdd } from './RegistrarInteresse.styles';
import GlobalVariablesConsumer from 'src/context/GlobalVariables';
import { registrarInteresse } from 'src/Fetch/FetchData';

const CATEGORIAS = ['Eletrônicos', 'Roupas', 'Alimentos'];

function RegistrarInteresse() {
    const { sessao, interesses, setInteresses } = GlobalVariablesConsumer();
    const [erro, setErro] = useState('');

    const handleAdd = async (categoria) => {
        try {
            const { interesses: atualizados } = await registrarInteresse(sessao, categoria);
            setInteresses(atualizados);
            setErro('');
        } catch (e) {
            setErro(e.message);
        }
    };

    return (
        <Page>
            <Title>Registrar Interesse</Title>
            {erro && <Sub style={{ color: '#e53e3e' }}>{erro}</Sub>}
            <List>
                {CATEGORIAS.map(c => {
                    const jaTem = interesses.includes(c);
                    return (
                        <Row key={c}>
                            <Info>
                                <Nome>{c}</Nome>
                                <Sub>{jaTem ? 'Interesse registrado' : 'Sem interesse'}</Sub>
                            </Info>
                            <BtnAdd onClick={() => handleAdd(c)} disabled={jaTem}>
                                {jaTem ? '✓ Adicionado' : '+ Adicionar'}
                            </BtnAdd>
                        </Row>
                    );
                })}
            </List>
        </Page>
    );
}

export default RegistrarInteresse;
