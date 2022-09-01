// src/mocks/handlers.js
import { rest } from 'msw'
import getLoginResponse from "./data/getLoginResponse"
import getWellKnown from "./data/getWellKnown"

export const handlers = [
    rest.get("https://matrix.org/_matrix/client/v3/login", async (req, res, ctx) => {
        const data = getLoginResponse;
        return res(ctx.status(200), ctx.json(data));
    }),
    rest.get("https://matrix.org/.well-known/matrix/client", async (req, res, ctx) => {
        const data = getWellKnown;
        console.log(data);
        return res(ctx.status(200), ctx.json(data));
    }),
]
