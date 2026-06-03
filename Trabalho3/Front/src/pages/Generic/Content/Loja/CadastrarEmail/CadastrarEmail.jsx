import React, { useState } from 'react';
import { Page, Title, Card, Group, Label, Input, ErrorMsg, Button } from './CadastrarEmail.styles';

function CadastrarEmail() {
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');

    const validate = () => {
        if (!email.trim()) { setError('Campo obrigatório'); return false; }
        setError('');
        return true;
    };

    const handleSubmit = () => {
        if (!validate()) return;
    };

    return (
        <Page>
            <Title>Informar Email</Title>
            <Card>
                <Group>
                    <Label>Email da Loja</Label>
                    <Input
                        type="email"
                        $hasError={!!error}
                        placeholder="loja@exemplo.com"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                    />
                    {error && <ErrorMsg>{error}</ErrorMsg>}
                </Group>
                <Button onClick={handleSubmit}>Salvar</Button>
            </Card>
        </Page>
    );
}

export default CadastrarEmail;
