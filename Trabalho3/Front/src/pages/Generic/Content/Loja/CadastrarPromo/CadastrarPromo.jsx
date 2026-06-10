import React, { useState } from 'react';
import { Page, Title, Card, Group, Label, Input, ErrorMsg, Button } from './CadastrarPromo.styles';
import GlobalVariablesConsumer from 'src/context/GlobalVariables';
import { cadastrarPromocao } from 'src/Fetch/FetchData';

const CATEGORIAS = ['Eletrônicos', 'Roupas', 'Alimentos'];

function CadastrarPromo() {
    const { lojaEmail } = GlobalVariablesConsumer();
    const [nome, setNome] = useState('');
    const [descricao, setDescricao] = useState('');
    const [categoria, setCategoria] = useState(CATEGORIAS[0]);
    const [errors, setErrors] = useState({});
    const [feedback, setFeedback] = useState('');

    const validate = () => {
        const e = {};
        if (!nome.trim())      e.nome = 'Campo obrigatório';
        if (!descricao.trim()) e.descricao = 'Campo obrigatório';
        setErrors(e);
        return Object.keys(e).length === 0;
    };

    const handleSubmit = async () => {
        setFeedback('');
        if (!validate()) return;
        try {
            await cadastrarPromocao({ nome, descricao, categoria, email: lojaEmail });
            setFeedback('Promoção enviada com sucesso!');
            setNome('');
            setDescricao('');
        } catch (err) {
            setFeedback(`Erro: ${err.message}`);
        }
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
                <Group>
                    <Label>Categoria</Label>
                    <Input as="select" value={categoria} onChange={e => setCategoria(e.target.value)}>
                        {CATEGORIAS.map(c => <option key={c} value={c}>{c}</option>)}
                    </Input>
                </Group>
                <Button onClick={handleSubmit}>Cadastrar</Button>
                {feedback && <ErrorMsg as="div" style={{ color: feedback.startsWith('Erro') ? '#e53e3e' : '#48bb78' }}>{feedback}</ErrorMsg>}
            </Card>
        </Page>
    );
}

export default CadastrarPromo;
