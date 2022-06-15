import PropTypes from 'prop-types'
import React from 'react'

const Images = {
	'apple': require('../assets/img/apple.svg').default,
	'github': require('../assets/img/github.svg').default,
	'facebook': require('../assets/img/facebook.svg').default,
	'google': require('../assets/img/google.svg').default,
	'gitlab': require('../assets/img/gitlab.svg').default
}

function validateAndReturnURL(url) {
	var pattern = /^((http|https):\/\/)/;
	if(!pattern.test(url)) {
		url = "https://" + url;
	}
	return url;
}

function AuthButton({ imgUrl, idpId, homeServer }){

	async function handleClick() {
		const baseUrl = validateAndReturnURL(homeServer);
		const redirectUrl = 'http://localhost:80/login-success'
		const endpoint = '_matrix/client/v3/login/sso/redirect/' + idpId + '?redirectUrl=' + redirectUrl;
		const fullUrl = new URL(endpoint, baseUrl);

		window.location.href = fullUrl;
	}

	return (
		<button
			className="block h-8 w-8 mx-4 rounded-full overflow-hidden border-2 border-gray-300 hover:border-white"
			type="button"
			onClick={handleClick}
			style={{ transition: "all .15s ease" }}
		>
			<img
			alt="..."
			className="h-full w-full mr-1"
			src={imgUrl}
			/>
		</button>
	)
}

AuthButton.propTypes = {
	imgUrl: PropTypes.string
}

export default function SSOLogin({ ssoProviders, homeServer }) {
	return (
		<div className={ssoProviders.length > 0 ? '' : 'hidden'}>
			<div className="btn-wrapper flex items-center justify-center">
				{ssoProviders.map((value) => {
					return <AuthButton imgUrl={Images[value.brand]} idpId={value.id} homeServer={homeServer} key={value.id} />
				})}
			</div>
		</div>
	)
}

SSOLogin.propTypes = {
	ssoProviders: PropTypes.array
}
