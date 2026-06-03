import React from 'react';
import GlobalVariablesConsumer from 'src/context/GlobalVariables';
import CadastrarPromo from 'src/pages/Generic/Content/Loja/CadastrarPromo/CadastrarPromo';
import CadastrarEmail from 'src/pages/Generic/Content/Loja/CadastrarEmail/CadastrarEmail';
import { Placeholder } from './Loja.styles';

const contentMap = {
    cadastrarPromo: <CadastrarPromo />,
    cadastrarEmail: <CadastrarEmail />,
};

function Loja() {
    const { menu } = GlobalVariablesConsumer();
    return contentMap[menu] ?? <Placeholder>Selecione uma opção no menu lateral.</Placeholder>;
}

export default Loja;
