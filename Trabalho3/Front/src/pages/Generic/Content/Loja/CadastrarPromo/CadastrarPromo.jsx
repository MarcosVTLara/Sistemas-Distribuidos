import React, { useState } from 'react';
import { Page, Title, Card, Group, Label, Input, ErrorMsg, Button } from './CadastrarPromo.styles';

function CadastrarPromo() {
    const [nome, setNome] = useState('');
    const [descricao, setDescricao] = useState('');
    const [errors, setErrors] = useState({});

    const validate = () => {
        const e = {};
        if (!nome.trim())      e.nome = 'Campo obrigatório';
        if (!descricao.trim()) e.descricao = 'Campo obrigatório';
        setErrors(e);
        return Object.keys(e).length === 0;
    };

    const handleSubmit = () => {
        if (!validate()) return;
    };

    return (
        <Page>
            <Title>Cadastrar Promoção</Title>
            <Card>
                <Group>
                    <Label>Nome da Promoção</Label>
                    <Input
                        $hasError={!!errors.nome}
                        placeholder="Ex: 50% off em eletrônicos"
                        value={nome}
                        onChange={e => setNome(e.target.value)}
                    />
                    {errors.nome && <ErrorMsg>{errors.nome}</ErrorMsg>}
                </Group>
                <Group>
                    <Label>Descrição</Label>
                    <Input
                        $hasError={!!errors.descricao}
                        placeholder="Descreva a promoção"
                        value={descricao}
                        onChange={e => setDescricao(e.target.value)}
                    />
                    {errors.descricao && <ErrorMsg>{errors.descricao}</ErrorMsg>}
                </Group>
                <Button onClick={handleSubmit}>Cadastrar</Button>
            </Card>
        </Page>
    );
}

export default CadastrarPromo;
