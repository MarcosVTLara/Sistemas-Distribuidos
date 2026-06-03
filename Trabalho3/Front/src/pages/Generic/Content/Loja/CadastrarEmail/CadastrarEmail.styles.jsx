import styled from 'styled-components';

export const Page = styled.div`
    padding: 2rem;
    font-family: sans-serif;
    max-width: 480px;
`;

export const Title = styled.h2`
    font-size: 1.5rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 1.5rem;
`;

export const Card = styled.div`
    background-color: #fff;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
`;

export const Group = styled.div`
    margin-bottom: 1.25rem;
`;

export const Label = styled.label`
    display: block;
    font-size: 0.875rem;
    font-weight: 600;
    color: #444;
    margin-bottom: 0.4rem;
`;

export const Input = styled.input`
    width: 100%;
    padding: 0.6rem 0.75rem;
    border-radius: 8px;
    border: 1.5px solid ${({ $hasError }) => ($hasError ? '#e53e3e' : '#ddd')};
    font-size: 0.95rem;
    outline: none;
    box-sizing: border-box;
    transition: border-color 0.15s;

    &:focus {
        border-color: ${({ $hasError }) => ($hasError ? '#e53e3e' : '#4361ee')};
    }
`;

export const ErrorMsg = styled.span`
    color: #e53e3e;
    font-size: 0.8rem;
    margin-top: 0.25rem;
    display: block;
`;

export const Button = styled.button`
    margin-top: 0.5rem;
    width: 100%;
    padding: 0.75rem;
    border-radius: 8px;
    border: none;
    background-color: #4361ee;
    color: #fff;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.15s;

    &:hover {
        background-color: #3451d1;
    }
`;
