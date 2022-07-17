import './App.css';
import React, { useState } from 'react';
import {Routes, Route, BrowserRouter, Outlet} from "react-router-dom";
import AccountSettings from './Pages/AccountSettings';
import RoomSettings from './Pages/RoomSettings';
import ServerSettings from './Pages/ServerSettings';
import Login from './Pages/Login';
import LoginSuccess from './Pages/LoginSuccess';
import ErrorPage from './Pages/ErrorPage';
import ExternalUrl from './Pages/ExternalUrl';
import CustomRouter from './Components/CustomRouter';
import history from './HelperFunctions/customHistory';
import { GlobalContext } from './GlobalContext';
import LayoutsWithNavbar from './Components/LayoutsWithNavbar';
import Logout from './Pages/Logout';
import GithubOauth from './Pages/GithubOauth';
import Room from './Pages/Room';
import RoomExternalUrl from './Pages/RoomExternalUrl';

export default function App() {
  const [matrixUserId, setMatrixUserId] = useState('');
  const [githubUserId, setGithubUserId] = useState('');

  return (
    <CustomRouter history={history}>
    <GlobalContext.Provider
          value = {{matrixUserId, setMatrixUserId, githubUserId, setGithubUserId}}>
      <Routes>
          <Route element={<LayoutsWithNavbar/>}>
            <Route path="/" element={<AccountSettings />} />
            <Route path="/room-settings" element={<RoomSettings />} />
            <Route path="/server-settings" element={<ServerSettings />} />
            <Route path="/logout" element={<Logout />} />
            <Route path="/rooms/:roomId" element={<Room />} />
            <Route path="/rooms/:roomId/external-url" element={<RoomExternalUrl />} />
          </Route>

        <Route path="/i/:url_code" element={<ExternalUrl />} />
        <Route path="/oauth2/github" element={<GithubOauth />} />
        <Route path="/login" element={<Login />} />
        <Route path="/login-success" element={<LoginSuccess/>} />
        <Route path="*" element={<ErrorPage/>} />
      </Routes>
    </GlobalContext.Provider>
    </CustomRouter>
  )
};
