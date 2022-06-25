import axios from "./HelperFunctions/customAxios";

export class MatrixApi {
    constructor(baseUrl) {
        this._baseUrl = baseUrl;
    }

    login(type, data = {}) {
        const fullUrl = new URL("/_matrix/client/v3/login", this._baseUrl);
        switch(type) {
            case "GET": {
                return axios.get(fullUrl);
            }

            case "POST": {
                return axios.post(fullUrl, data);
            }
        }
    }

    wellKnown(type, data={}) {
        const fullUrl = new URL(".well-known/matrix/client", this._baseUrl);
        switch(type) {
            case "GET": {
                return axios.get(fullUrl);
            }
        }
    }

    requestOpenIdToken(type, baseUrl, data) {
        const fullUrl = new URL(`/_matrix/client/v3/user/${data.user_id}/openid/request_token`, baseUrl);
        switch(type) {
            case "POST": {
                return axios.post(fullUrl, {}, {
                    headers: {
                        'Authorization': `Bearer ${data.access_token}`
                    }
                })
            }
        }
    }

    parseMedia(mxcUrl) {
        const [serverName, mediaId] = mxcUrl.replace('mxc://', '').split('/');
        const endpoint = `_matrix/media/v3/download/${serverName}/${mediaId}`;

        return new URL(endpoint, this._baseUrl);
    }

    ssoRedirectUrl(id, redirectUrl){
		const endpoint = '_matrix/client/v3/login/sso/redirect/' + id + '?redirectUrl=' + redirectUrl;
		const imgUrl =  new URL(endpoint, this._baseUrl);
        return imgUrl.href;
    }
}
