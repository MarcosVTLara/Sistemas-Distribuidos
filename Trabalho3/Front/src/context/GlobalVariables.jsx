import React from 'react';
import userTypes from 'src/constants/userTypes.json'
const globalVariablesContext = React.createContext();

function useGlobalVariables(){
    const [login, setLogin] = React.useState(userTypes[0])
    const [menu, setMenu] = React.useState(userTypes[0])
    return{
        login,
        menu,

        newLogin(newUser){
            return new Promise((resolve) => {
                setLogin(newUser);
                resolve();
            })
        },

        newMenu(newUser){
            return new Promise((resolve) => {
                setMenu(newUser);
                resolve();
            })
        }
    };
}
export function GlobalVariablesProvider({ children }){
    const auth = useGlobalVariables();
    return(
        <globalVariablesContext.Provider value={auth}>
            {children}
        </globalVariablesContext.Provider>
    );
}

export default function GlobalVariavblesConsumer(){
    return React.useContext(globalVariablesContext);
}