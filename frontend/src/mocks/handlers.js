// src/mocks/handlers.js
import { rest } from 'msw'
import getLoginResponse from "./data/getLoginResponse"
import getWellKnown from "./data/getWellKnown"
import openIdTokenResponse from "./data/openIdTokenResponse"

const defaultHomeserver = "https://matrix.org";

export const handlers = [
    rest.get(`${defaultHomeserver}/_matrix/client/v3/login`, async (req, res, ctx) => {
        const data = getLoginResponse;
        return res(ctx.status(200), ctx.json(data));
    }),
    rest.get(`${defaultHomeserver}/.well-known/matrix/client`, async (req, res, ctx) => {
        const data = getWellKnown;
        return res(ctx.status(200), ctx.json(data));
    }),
    rest.post(`${defaultHomeserver}/_matrix/client/v3/user/:userId/openid/request_token`, async (req, res, ctx) => {
        const { userId } = req.params;
        const data = openIdTokenResponse;
        return res(ctx.status(200), ctx.json(data));
    }),
    rest.post("/api/verify-openid", async (req, res, ctx) => {
        const loginBody = await req.json();
        try{
            expect(loginBody).toStrictEqual(openIdTokenResponse);
        }
        catch (err) {
            console.log(err);
        }
        return res(ctx.status(200), ctx.json({}));
    })
]
