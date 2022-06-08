import './App.css';
import React from 'react';
import {Routes, Route, BrowserRouter} from "react-router-dom";
import Home from "./Pages/Home";
import AccountSettings from './Pages/AccountSettings';
import NavBar from './Components/NavBar';
import RoomSettings from './Pages/RoomSettings';
import ServerSettings from './Pages/ServerSettings';
import Login from './Pages/Login';


export default function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="account" element={<AccountSettings />} />
        <Route path="room-settings" element={<RoomSettings />} />
        <Route path="server-settings" element={<ServerSettings />} />
        <Route path="login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  )
};
