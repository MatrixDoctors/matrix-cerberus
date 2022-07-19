// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';
import { server } from './mocks/server';

beforeAll(() => server.listen())
// if you need to add a handler after calling setupServer for some specific test
// this will remove that handler for the rest of them
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
