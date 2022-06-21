export default function validateAndReturnUrl(url) {
	let validUrl;
	// Check for protocol.
	try {
		validUrl = new URL(url);
	}
	catch {
		validUrl = "https://" + url;
		validUrl = new URL(validUrl);
	}

	if (validUrl.protocol !==  "http:" &&  validUrl.protocol !==  "https:") {
		throw new Error("Invalid URL protocol");
	}

	// URL().href returns a url with a trailing '/'
	if (validUrl.origin + '/' !== validUrl.href){
		throw new Error("Invalid Homeserver URL");
	}

	return validUrl.origin;
}
