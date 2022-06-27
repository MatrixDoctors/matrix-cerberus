import './App.css';
import React, { useState } from 'react';
import {Routes, Route, BrowserRouter, Outlet} from "react-router-dom";
import AccountSettings from './Pages/AccountSettings';
import NavBar from './Components/NavBar';
import RoomSettings from './Pages/RoomSettings';
import ServerSettings from './Pages/ServerSettings';
import Login from './Pages/Login';
import LoginSuccess from './Pages/LoginSuccess';
import ErrorPage from './Pages/ErrorPage';
import ExternalUrl from './Pages/ExternalUrl';
import CustomRouter from './Components/CustomRouter';
import history from './HelperFunctions/customHistory';
import { GlobalContext } from './GlobalContext';

function LayoutsWithNavbar() {
  return (
    <>
      <NavBar />

      {/* This Outlet is the place in which react-router will render your components that you need with the navbar */}
      <Outlet />
    </>
  );
}

export default function App() {
  const [matrixUserId, setMatrixUserId] = useState('@kuries:matrix.org');

  return (
    <CustomRouter history={history}>
    <GlobalContext.Provider
          value = {{matrixUserId, setMatrixUserId}}>
      <Routes>
          <Route path='/' element={<LayoutsWithNavbar/>}>
            <Route path="/" element={<AccountSettings />} />
            <Route path="/room-settings" element={<RoomSettings />} />
            <Route path="/server-settings" element={<ServerSettings />} />
          </Route>

        <Route path="/i/:url_code" element={<ExternalUrl />} />
        <Route path="/login" element={<Login />} />
        <Route path="/login-success" element={<LoginSuccess/>} />
        <Route path="*" element={<ErrorPage/>} />
      </Routes>
    </GlobalContext.Provider>
    </CustomRouter>
  )
};
