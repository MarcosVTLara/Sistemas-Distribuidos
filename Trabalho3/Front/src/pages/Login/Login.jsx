import React from 'react';
import { useNavigate } from 'react-router-dom';
import GlobalVariablesConsumer from 'src/context/GlobalVariables';
import userTypes from 'src/constants/userTypes.json';
import { Page, Title, Subtitle, CardsContainer, CardUser, CardLoja, Icon } from './Login.styles';

function Login() {
    const { newLogin } = GlobalVariablesConsumer();
    const navigate = useNavigate();

    const handleLogin = async (type, route) => {
        await newLogin(type);
        navigate(route);
    };

    return (
        <Page>
            <Title>Bem-vindo</Title>
            <Subtitle>Selecione o tipo de acesso</Subtitle>
            <CardsContainer>
                <CardUser onClick={() => handleLogin(userTypes[1], '/user')}>
                    <Icon>👤</Icon>
                    Usuário
                </CardUser>
                <CardLoja onClick={() => handleLogin(userTypes[2], '/loja')}>
                    <Icon>🏪</Icon>
                    Loja
                </CardLoja>
            </CardsContainer>
        </Page>
    );
}

export default Login;
