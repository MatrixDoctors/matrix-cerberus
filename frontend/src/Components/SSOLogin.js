import PropTypes from 'prop-types'
import React from 'react'
import { MatrixApi } from '../MatrixApi';

const Images = {
	'apple': require('../assets/img/apple.svg').default,
	'github': require('../assets/img/github.svg').default,
	'facebook': require('../assets/img/facebook.svg').default,
	'google': require('../assets/img/google.svg').default,
	'gitlab': require('../assets/img/gitlab.svg').default,
	'default': require('../assets/img/globe-wire.svg').default
}

function AuthButton({ idp, homeServer }){

	async function handleClick() {
		const redirectUrl = `${process.env.REACT_APP_BASE_URL}/login-success`
		window.location.href = new MatrixApi(homeServer).ssoRedirectUrl(idp.id, redirectUrl);
	}

	let imgUrl, name = idp.name.toLowerCase();
	if(name in Images) {
		imgUrl = Images[name];
	}
	else {
		imgUrl = new MatrixApi(homeServer).parseMedia(idp.icon);
	}

	return (
		<button
			title={idp.name}
			aria-label={idp.name}
			className="block h-7 w-7 mx-4 rounded-full overflow-hidden border-2 border-gray-300 hover:border-white"
			type="button"
			onClick={handleClick}
			style={{ transition: "all .15s ease" }}
		>
			<img
			className="h-full w-full mr-1"
			src={imgUrl}
			onError={(e) => {
				if(e.target.src !== Images['default']){
					e.target.src = Images['default'];
				}
			}}
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

export default function SSOLogin({ ssoProviders }) {
	const homeServer = localStorage.getItem("homeServer");
	return (
		<div className="btn-wrapper flex items-center justify-center">
			{ssoProviders.map((value) => {
				return <AuthButton idp={value} homeServer={homeServer} key={value.id} />
			})}
		</div>
	)
}

SSOLogin.propTypes = {
	ssoProviders: PropTypes.array,
}
