export default function parseImageUrl(homeServer, mxcUrl) {
    const [serverName, mediaId] = mxcUrl.replace('mxc://', '').split('/');
    const baseUrl = homeServer;
    const endpoint = `_matrix/media/v3/download/${serverName}/${mediaId}`;

    return new URL(endpoint, baseUrl);
}
