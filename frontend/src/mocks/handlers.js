// src/mocks/handlers.js
import { rest } from 'msw'
import getLoginResponse from "./data/getLoginResponse"

export const handlers = [
    rest.get("https://matrix.org/_matrix/client/v3/login", async (req, res, ctx) => {
        const data = getLoginResponse;
        return res(ctx.status(200), ctx.json(data));
    }),
]
