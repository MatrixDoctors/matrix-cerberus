import { render, screen} from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { server, rest } from '../mocks/server';
import getLoginResponse from "../mocks/data/getLoginResponse"
import getWellKnown from "../mocks/data/getWellKnown"


import Login from './Login';
import CustomRouter from '../Components/CustomRouter';
import history from "../HelperFunctions/customHistory";
import React from 'react';

test('Render all the input fields and buttons', async () => {
  render(
    <CustomRouter history={history}>
      <Login />
    </CustomRouter>
  );

  // Checking SSO Providers
  expect(await screen.findByRole('button', {name: /Google/i})).toBeInTheDocument();
  expect(await screen.findByRole('button', {name: /Github/i})).toBeInTheDocument();

  expect(await screen.getByLabelText(/Homeserver/i)).toBeInTheDocument();

  expect(await screen.getByRole("button", {name: /save/i} )).toBeInTheDocument();

  expect(await screen.getByLabelText(/Sign in with/i)).toBeInTheDocument();

  expect(await screen.getByLabelText(/username/i)).toBeInTheDocument();

  expect(await screen.getByTestId(/password/i)).toBeInTheDocument();

  expect(await screen.getByRole("button", {name: /sign in/i} )).toBeInTheDocument();

});

test('Check input field change', async () => {
  const user = userEvent.setup();

  render(
    <CustomRouter history={history}>
      <Login />
    </CustomRouter>
  );

  await user.selectOptions(screen.getByRole('combobox'), 'Username');
  expect(await screen.getByLabelText(/username/i)).toBeInTheDocument();

  await user.selectOptions(screen.getByRole('combobox'), 'Email address');
  expect(await screen.getByLabelText(/email/i)).toBeInTheDocument();

  await user.selectOptions(screen.getByRole('combobox'), 'Phone');
  expect(await screen.getByLabelText('phone-number')).toBeInTheDocument();

});

test('When SSO Providers are not available', async () => {
  const user = userEvent.setup();
  server.use(
    rest.get("https://matrix.org/_matrix/client/v3/login", async (req, res, ctx) => {
      let data = getLoginResponse;
      data["flows"] = data["flows"].filter(item => item["type"] !== "m.login.sso");
      return res(ctx.status(200), ctx.json(data));
    }),
  )

  render(
    <CustomRouter history={history}>
      <Login />
    </CustomRouter>
  );

  // to prevent the no-wrapped-in-act warning.
  await user.click(document.body);

  // Checking SSO Providers
  expect(await screen.queryByRole('button', {name: /Google/i})).not.toBeInTheDocument();
  expect(await screen.queryByRole('button', {name: /Github/i})).not.toBeInTheDocument();

  expect(await screen.getByLabelText(/Homeserver/i)).toBeInTheDocument();

  expect(await screen.getByRole("button", {name: /save/i} )).toBeInTheDocument();

  expect(await screen.getByLabelText(/Sign in with/i)).toBeInTheDocument();

  expect(await screen.getByLabelText(/username/i)).toBeInTheDocument();

  expect(await screen.getByTestId(/password/i)).toBeInTheDocument();

  expect(await screen.getByRole("button", {name: /sign in/i} )).toBeInTheDocument();

});

test('When complete username is entered', async () => {
  const user = userEvent.setup();
  const exampleHomeserver = "https://example.org";

  server.use(
    rest.get(`${exampleHomeserver}/_matrix/client/v3/login`, async (req, res, ctx) => {
        const data = getLoginResponse;
        return res(ctx.status(200), ctx.json(data));
    }),
    rest.get(`${exampleHomeserver}/.well-known/matrix/client`, async (req, res, ctx) => {
        let data = getWellKnown;
        data["m.homeserver"]["base_url"] = exampleHomeserver;
        return res(ctx.status(200), ctx.json(data));
    }),
  )

  render(
    <CustomRouter history={history}>
      <Login />
    </CustomRouter>
  );

  // Focus on user field, enter the full username and go out of focus (blur)
  let field = screen.getByLabelText(/username/i);
  field.focus();
  await user.type(field, "@Hello:example.org");
  await user.click(document.body);

  expect(screen.getByLabelText(/username/i)).toHaveValue("@Hello:example.org");

  let homeserver = screen.getByLabelText(/homeserver/i);
  const shortenedHomeserverUrl = exampleHomeserver.replace('https://', '');

  // This is kind of a hackish way to trigger the input field update of homserver url.
  await user.click(homeserver);
  expect(screen.getByLabelText(/Homeserver/i)).toHaveValue(shortenedHomeserverUrl);

});
