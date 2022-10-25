import axios from 'axios';
import React, { useContext, useEffect } from 'react'
import { Outlet, useNavigate } from 'react-router-dom';
import { GlobalContext } from '../GlobalContext';
import NavBar from './NavBar';

export default function LayoutsWithNavbar() {
  const {setMatrixUserId, setGithubUserId} = useContext(GlobalContext);
  const navigate = useNavigate();

  useEffect( () => {
      const fetchCurrentUser = async () => {
        const resp = await axios.get('/api/current-user');
        if(resp.data.matrix_user_id !== null){
            const matrixUserId = resp.data.matrix_user_id;
            const githubUserId = resp.data.github_user_id ? resp.data.github_user_id : "";

            console.log(`Logged in as ${resp.data.matrix_user_id}!`);

            setMatrixUserId(matrixUserId);
            setGithubUserId(githubUserId);
        }
        else {
          navigate('/login');
        }
      }
      fetchCurrentUser();
  }, []);

  return (
    <>
      <NavBar />
      <Outlet />
    </>
  );
}
