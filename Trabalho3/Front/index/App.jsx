import React from 'react';
import ReactDOM from 'react-dom/client';
import App from 'src/App';
import { GlobalVariablesProvider } from 'src/context/GlobalVariables';
// import FetchData from 'src/threads/FetchData/FetchData';


const rootElement = document.getElementById('app');
const root = ReactDOM.createRoot(rootElement);

root.render(
<GlobalVariablesProvider>
    {/* <FetchData /> */}
    <App />
</GlobalVariablesProvider>
);