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
    padding: 1rem 1.25rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
`;

export const Tag = styled.span`
    font-size: 0.75rem;
    font-weight: 700;
    color: #4361ee;
    text-transform: uppercase;
    letter-spacing: 0.04em;
`;

export const Message = styled.span`
    font-size: 0.95rem;
    color: #222;
`;

export const Time = styled.span`
    font-size: 0.75rem;
    color: #999;
    align-self: flex-end;
`;

export const Empty = styled.p`
    color: #888;
    font-size: 0.95rem;
    padding: 1rem 0;
`;
