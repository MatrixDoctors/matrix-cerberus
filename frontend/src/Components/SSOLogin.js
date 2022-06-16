import PropTypes from 'prop-types'
import React from 'react'

const Images = {
	'apple': require('../assets/img/apple.svg').default,
	'github': require('../assets/img/github.svg').default,
	'facebook': require('../assets/img/facebook.svg').default,
	'google': require('../assets/img/google.svg').default,
	'gitlab': require('../assets/img/gitlab.svg').default
}

function AuthButton({ imgUrl }){
	return (
		<button
			className="block h-8 w-8 mx-4 rounded-full overflow-hidden border-2 border-gray-300 hover:border-white"
			type="button"
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

export default function SSOLogin({ ssoProviders }) {
	return (
		<div className={ssoProviders.length > 0 ? '' : 'hidden'}>
			<div className="btn-wrapper flex items-center justify-center">
				{ssoProviders.map((name) => {
					return <AuthButton imgUrl={Images[name]} key={`${name}`} />
				})}
			</div>
		</div>
	)
}

SSOLogin.propTypes = {
	ssoProviders: PropTypes.array
}
