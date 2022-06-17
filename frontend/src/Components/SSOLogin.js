import PropTypes from 'prop-types'
import React from 'react'
import validateAndReturnUrl from '../HelperFunctions/validateAndReturnUrl';
import parseImageUrl from '../HelperFunctions/parseImageUrl';

const Images = {
	'apple': require('../assets/img/apple.svg').default,
	'github': require('../assets/img/github.svg').default,
	'facebook': require('../assets/img/facebook.svg').default,
	'google': require('../assets/img/google.svg').default,
	'gitlab': require('../assets/img/gitlab.svg').default
}

function AuthButton({ idp, homeServer }){

	async function handleClick() {
		const baseUrl = validateAndReturnUrl(homeServer);
		const redirectUrl = 'http://localhost:80/login-success'
		const endpoint = '_matrix/client/v3/login/sso/redirect/' + idp.id + '?redirectUrl=' + redirectUrl;
		const fullUrl = new URL(endpoint, baseUrl);

		window.location.href = fullUrl;
	}

	const imgUrl = parseImageUrl(homeServer, idp.icon);

	return (
		<button
			className="block h-7 w-7 mx-4 rounded-full overflow-hidden border-2 border-gray-300 hover:border-white"
			type="button"
			onClick={handleClick}
			style={{ transition: "all .15s ease" }}
		>
			<img
			alt="..."
			className="h-full w-full mr-1"
			src={imgUrl.href}
			/>
		</button>
	)
}

AuthButton.propTypes = {
	idp: PropTypes.shape({
		id: PropTypes.string,
		icon: PropTypes.string,
		brand: PropTypes.string,
		name: PropTypes.string
	}),
	homeServer: PropTypes.string
}

export default function SSOLogin({ ssoProviders, homeServer }) {
	return (
		<div className={ssoProviders.length > 0 ? '' : 'hidden'}>
			<div className="btn-wrapper flex items-center justify-center">
				{ssoProviders.map((value) => {
					return <AuthButton idp={value} homeServer={homeServer} key={value.id} />
				})}
			</div>
		</div>
	)
}

SSOLogin.propTypes = {
	ssoProviders: PropTypes.array,
	homeServer: PropTypes.string
}
