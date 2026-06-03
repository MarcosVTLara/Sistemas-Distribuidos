import React from 'react';
import { useOutlet } from 'react-router-dom';
import styled from 'styled-components';

const Placeholder = styled.div`
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #888;
    font-size: 1rem;
    font-family: sans-serif;
`;

function Generic() {
    const outlet = useOutlet();
    return outlet ?? <Placeholder>Selecione uma opção no menu lateral.</Placeholder>;
}

export default Generic;
