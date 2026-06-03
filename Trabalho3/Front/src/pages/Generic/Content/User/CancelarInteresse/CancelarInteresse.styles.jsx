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
    gap: 0.6rem;
`;

export const Row = styled.div`
    background-color: #fff;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
    display: flex;
    align-items: center;
    justify-content: space-between;
`;

export const Info = styled.div`
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
`;

export const Nome = styled.span`
    font-size: 0.95rem;
    font-weight: 600;
    color: #1a1a2e;
`;

export const Sub = styled.span`
    font-size: 0.78rem;
    color: #888;
`;

export const BtnRemove = styled.button`
    padding: 0.45rem 1rem;
    border-radius: 8px;
    border: none;
    background-color: #fc5c65;
    color: #fff;
    font-weight: 600;
    cursor: pointer;
    font-size: 0.875rem;
    transition: background-color 0.15s;

    &:hover {
        background-color: #e53e3e;
    }
`;

export const Empty = styled.p`
    color: #888;
    font-size: 0.95rem;
    padding: 1rem 0;
`;
