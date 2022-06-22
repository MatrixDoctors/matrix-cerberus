import './App.css';
import React from 'react';
import {Routes, Route, BrowserRouter, Outlet} from "react-router-dom";
import AccountSettings from './Pages/AccountSettings';
import NavBar from './Components/NavBar';
import RoomSettings from './Pages/RoomSettings';
import ServerSettings from './Pages/ServerSettings';
import Login from './Pages/Login';
import LoginSuccess from './Pages/LoginSuccess';
import ErrorPage from './Pages/ErrorPage';

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
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<LayoutsWithNavbar/>}>
          <Route path="/" element={<AccountSettings />} />
          <Route path="/room-settings" element={<RoomSettings />} />
          <Route path="/server-settings" element={<ServerSettings />} />
          <Route path="/login-success" element={<LoginSuccess/>} />
        </Route>

        <Route path="/login" element={<Login />} />
        <Route path="*" element={<ErrorPage/>} />
      </Routes>
    </BrowserRouter>
  )
};
