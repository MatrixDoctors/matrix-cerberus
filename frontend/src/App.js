import './App.css';
import React from 'react';
import {Routes, Route, BrowserRouter} from "react-router-dom";
import AccountSettings from './Pages/AccountSettings';
import NavBar from './Components/NavBar';
import RoomSettings from './Pages/RoomSettings';
import ServerSettings from './Pages/ServerSettings';
import Login from './Pages/Login';
import LoginSuccess from './Pages/LoginSuccess';


export default function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route path="/" element={<AccountSettings />} />
        <Route path="/room-settings" element={<RoomSettings />} />
        <Route path="/server-settings" element={<ServerSettings />} />
        <Route path="/login" element={<Login />} />
        <Route path="/login-success" element={<LoginSuccess/>} />
      </Routes>
    </BrowserRouter>
  )
};
