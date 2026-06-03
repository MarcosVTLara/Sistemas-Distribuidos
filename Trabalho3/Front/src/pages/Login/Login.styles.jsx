import styled from 'styled-components';

export const Page = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: #f0f2f5;
    font-family: sans-serif;
`;

export const Title = styled.h1`
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
    color: #1a1a2e;
`;

export const Subtitle = styled.p`
    color: #666;
    margin-bottom: 3rem;
    font-size: 1rem;
`;

export const CardsContainer = styled.div`
    display: flex;
    gap: 2rem;
`;

const Card = styled.button`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 180px;
    height: 180px;
    border-radius: 16px;
    border: none;
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: transform 0.15s, box-shadow 0.15s;

    &:hover {
        transform: translateY(-4px);
    }
`;

export const CardUser = styled(Card)`
    background-color: #4361ee;
    color: #fff;

    &:hover {
        box-shadow: 0 8px 25px rgba(67, 97, 238, 0.4);
    }
`;

export const CardLoja = styled(Card)`
    background-color: #3f8efc;
    color: #fff;

    &:hover {
        box-shadow: 0 8px 25px rgba(63, 142, 252, 0.4);
    }
`;

export const Icon = styled.span`
    font-size: 2.5rem;
    margin-bottom: 0.75rem;
`;
