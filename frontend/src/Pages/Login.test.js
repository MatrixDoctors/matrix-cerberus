import { render, screen } from '@testing-library/react';
import Login from './Login';
import CustomRouter from '../Components/CustomRouter';
import history from "../HelperFunctions/customHistory";
import React from 'react';

test('renders all the input fields and buttons', () => {
  render(
    <CustomRouter history={history}>
      <Login />
    </CustomRouter>
  );
  const homeServer = screen.getByLabelText(/Homeserver/i);
  expect(homeServer).toBeInTheDocument();

  const saveButton = screen.getByRole("button", {name: /save/i} );
  expect(saveButton).toBeInTheDocument();

  const selectField = screen.getByLabelText(/Sign in with/i);
  expect(selectField).toBeInTheDocument();

  const userField = screen.getByTestId(/username/i);
  expect(userField).toBeInTheDocument();

  const password = screen.getByTestId(/password/i);
  expect(password).toBeInTheDocument();

  const signInButton = screen.getByRole("button", {name: /sign in/i} );
  expect(signInButton).toBeInTheDocument();

});
