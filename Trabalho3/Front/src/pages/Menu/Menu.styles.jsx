import styled from 'styled-components';

export const Aside = styled.aside`
    width: 220px;
    min-height: 100vh;
    background-color: #1a1a2e;
    color: #fff;
    display: flex;
    flex-direction: column;
    font-family: sans-serif;
    flex-shrink: 0;
`;

export const Header = styled.div`
    padding: 1.5rem 1rem 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
`;

export const Role = styled.p`
    font-size: 0.75rem;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0 0 0.25rem;
`;

export const Name = styled.h2`
    font-size: 1.1rem;
    font-weight: 700;
    margin: 0;
`;

export const Nav = styled.nav`
    display: flex;
    flex-direction: column;
    padding: 1rem 0.75rem;
    gap: 0.25rem;
`;

export const Item = styled.button`
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.65rem 0.75rem;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: ${({ $active }) => ($active ? '600' : '400')};
    background-color: ${({ $active }) => ($active ? 'rgba(67, 97, 238, 0.35)' : 'transparent')};
    color: ${({ $active }) => ($active ? '#fff' : '#ccc')};
    text-align: left;
    transition: background 0.15s, color 0.15s;

    &:hover {
        background-color: ${({ $active }) => ($active ? 'rgba(67, 97, 238, 0.35)' : 'rgba(255, 255, 255, 0.07)')};
        color: #fff;
    }
`;

export const ItemIcon = styled.span`
    font-size: 1rem;
    min-width: 1.25rem;
    text-align: center;
`;
