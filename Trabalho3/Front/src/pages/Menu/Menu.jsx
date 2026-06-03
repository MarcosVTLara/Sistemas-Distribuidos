import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import GlobalVariablesConsumer from 'src/context/GlobalVariables';
import userTypes from 'src/constants/userTypes.json';
import { Aside, Header, Role, Name, Nav, Item, ItemIcon } from './Menu.styles';
import configMenu from './configMenu.json';

function Menu() {
    const { login } = GlobalVariablesConsumer();
    const navigate = useNavigate();
    const { pathname } = useLocation();

    const isLoja = login === userTypes[2];
    const basePath = isLoja ? '/loja' : '/user';
    const items = isLoja ? configMenu["Loja"] : configMenu["User"];

    return (
        <Aside>
            <Header>
                <Role>Logado como</Role>
                <Name>{login}</Name>
            </Header>
            <Nav>
                {items.map(item => (
                    <Item
                        key={item.key}
                        $active={pathname === `${basePath}/${item.key}`}
                        onClick={() => navigate(`${basePath}/${item.key}`)}
                    >
                        <ItemIcon>{item.icon}</ItemIcon>
                        {item.label}
                    </Item>
                ))}
            </Nav>
        </Aside>
    );
}

export default Menu;
