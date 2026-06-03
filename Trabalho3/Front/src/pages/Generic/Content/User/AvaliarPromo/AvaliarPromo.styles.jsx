import styled from 'styled-components';

export const Page = styled.div`
    padding: 2rem;
    font-family: sans-serif;
    max-width: 640px;
`;

export const Title = styled.h2`
    font-size: 1.5rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 1.5rem;
`;

export const List = styled.div`
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
`;

export const Card = styled.div`
    background-color: #fff;
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
`;

export const Tag = styled.div`
    font-size: 0.75rem;
    font-weight: 700;
    color: #4361ee;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.3rem;
`;

export const Nome = styled.div`
    font-size: 1rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 0.2rem;
`;

export const Desc = styled.div`
    font-size: 0.875rem;
    color: #555;
    margin-bottom: 1rem;
`;

export const Buttons = styled.div`
    display: flex;
    gap: 0.75rem;
`;

const VoteBtn = styled.button`
    flex: 1;
    padding: 0.55rem;
    border-radius: 8px;
    border: none;
    color: #fff;
    font-weight: 600;
    cursor: pointer;
    font-size: 0.9rem;
    transition: opacity 0.15s;

    &:hover {
        opacity: 0.85;
    }
`;

export const BtnPos = styled(VoteBtn)`
    background-color: #48bb78;
`;

export const BtnNeg = styled(VoteBtn)`
    background-color: #fc5c65;
`;

export const Votos = styled.div`
    font-size: 0.78rem;
    color: #888;
    margin-top: 0.6rem;
`;
