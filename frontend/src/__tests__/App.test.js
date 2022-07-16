import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../App';
import React from 'react';

test('renders Page Not Found', () => {
  const badRoute = '/some/bad/route'
  render(
    <MemoryRouter initialEntries={[badRoute]}>
      <App />
    </MemoryRouter>
  );
  const linkElement = screen.getByText("Looks like you've entered the wrong doorway.");
  expect(linkElement).toBeInTheDocument();
});
