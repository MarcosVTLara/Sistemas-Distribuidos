import React from 'react';
import GlobalVariablesConsumer from 'src/context/GlobalVariables';
import Feed from 'src/pages/Generic/Content/User/Feed/Feed';
import AvaliarPromo from 'src/pages/Generic/Content/User/AvaliarPromo/AvaliarPromo';
import RegistrarInteresse from 'src/pages/Generic/Content/User/RegistrarInteresse/RegistrarInteresse';
import CancelarInteresse from 'src/pages/Generic/Content/User/CancelarInteresse/CancelarInteresse';
import { Placeholder } from './User.styles';

const contentMap = {
    feed:               <Feed />,
    avaliarPromo:       <AvaliarPromo />,
    registrarInteresse: <RegistrarInteresse />,
    cancelarInteresse:  <CancelarInteresse />,
};

function User() {
    const { menu } = GlobalVariablesConsumer();
    return contentMap[menu] ?? <Placeholder>Selecione uma opção no menu lateral.</Placeholder>;
}

export default User;
