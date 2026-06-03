import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';

import Menu from 'src/pages/Menu/Menu';
import Login from 'src/pages/Login/Login';
import Generic from 'src/pages/Generic/Generic';
import CadastrarPromo from 'src/pages/Generic/Content/Loja/CadastrarPromo/CadastrarPromo';
import CadastrarEmail from 'src/pages/Generic/Content/Loja/CadastrarEmail/CadastrarEmail';
import Feed from 'src/pages/Generic/Content/User/Feed/Feed';
import AvaliarPromo from 'src/pages/Generic/Content/User/AvaliarPromo/AvaliarPromo';
import RegistrarInteresse from 'src/pages/Generic/Content/User/RegistrarInteresse/RegistrarInteresse';
import CancelarInteresse from 'src/pages/Generic/Content/User/CancelarInteresse/CancelarInteresse';
import { Layout, Content } from './RouterFront.styles';

function AppLayout() {
    return (
        <Layout>
            <Menu />
            <Content>
                <Outlet />
            </Content>
        </Layout>
    );
}

function RouterFront() {
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route element={<AppLayout />}>
                    <Route path="/loja" element={<Generic />}>
                        <Route path="cadastrarPromo" element={<CadastrarPromo />} />
                        <Route path="cadastrarEmail" element={<CadastrarEmail />} />
                    </Route>
                    <Route path="/user" element={<Generic />}>
                        <Route path="feed" element={<Feed />} />
                        <Route path="avaliarPromo" element={<AvaliarPromo />} />
                        <Route path="registrarInteresse" element={<RegistrarInteresse />} />
                        <Route path="cancelarInteresse" element={<CancelarInteresse />} />
                    </Route>
                </Route>
                <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
        </Router>
    );
}

export default RouterFront;
