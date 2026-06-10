import React, { useState } from 'react';
import { Page, Title, Card, Group, Label, Input, ErrorMsg, Button } from './CadastrarEmail.styles';
import GlobalVariablesConsumer from 'src/context/GlobalVariables';

function CadastrarEmail() {
    const { lojaEmail, salvarLojaEmail } = GlobalVariablesConsumer();
    const [email, setEmail] = useState(lojaEmail);
    const [error, setError] = useState('');
    const [feedback, setFeedback] = useState('');

    const validate = () => {
        if (!email.trim()) { setError('Campo obrigatório'); return false; }
        setError('');
        return true;
    };

    const handleSubmit = () => {
        setFeedback('');
        if (!validate()) return;
        salvarLojaEmail(email.trim());
        setFeedback('Email salvo! Será usado para notificar hot deals.');
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
                {feedback && <ErrorMsg as="div" style={{ color: '#48bb78' }}>{feedback}</ErrorMsg>}
            </Card>
        </Page>
    );
}

export default CadastrarEmail;
