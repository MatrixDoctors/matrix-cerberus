export default function validateAndReturnUrl(url) {
	var pattern = /^((http|https):\/\/)/;
	if(!pattern.test(url)) {
		url = "https://" + url;
	}
	return url;
}