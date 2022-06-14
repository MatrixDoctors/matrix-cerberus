import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import PropTypes from "prop-types"

import axios from 'axios'

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

function UserField({ type, onBlur }) {
	switch (type) {
		case 'Email address': {
			return (
				<div className="w-full mb-3">
					<input
					type="email"
					className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
					placeholder="Email"
					style={{ transition: "all .15s ease" }}
					/>
				</div>
			)
		}

		case 'Phone': {
			return (
				<div className="flex items-center justify-start mb-3">
					<input
					type="tel"
					className="block mr-1 px-3 py-3 w-1/5 border-0 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring"
					placeholder='+1'
					style={{ transition: "all .15s ease" }}
					/>
					<input
					type="tel"
					className="block border-0 px-3 py-3 w-4/5 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring"
					placeholder="Phone"
					style={{ transition: "all .15s ease" }}
					/>
				</div>
			)
		}
		// Username is default.
		default: {
			return (
				<div className="w-full mb-3">
					<input
					type="username"
					className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
					placeholder="Username"
					style={{ transition: "all .15s ease" }}
					onBlur={onBlur}
					/>
				</div>
			)
		} 
	}
}

UserField.propTypes = {
	type: PropTypes.string
}

function SSOLogin({ ssoProviders, errorMessage }) {
	return (
		<div className="rounded-t mb-0 px-6 py-6">
			<div className="text-center mb-3">
			<h6 className="text-gray-600 text-md font-bold">
				{ssoProviders.length > 0 ? 'Sign in with' : 'Sign In'}
			</h6>
			</div>

			{/* Error Message Display */}
			<div className="text-center mb-3">
				<p className="text-red-600 text-sm">
					{errorMessage}
				</p>
			</div>

			{/* Button Wrapper */}
			<div className={ssoProviders.length > 0 ? '' : 'hidden'}>
				<div className="btn-wrapper flex items-center justify-center">
					{ssoProviders.map((name) => {
						return <AuthButton imgUrl={Images[name]} key={`${name}`} />
					})}
				</div>
			</div>
			<hr className="mt-6 border-b-1 border-gray-400" />	
		</div>
	)
}

export default function Login() {

	// Used to set the Identifier type for password based login
	const [fieldType, setFieldType] = useState('Username');

	// Updated every time the homeserver input text is changed.
	const [inputHomeServer, setInputHomeServer] = useState('matrix.org');

	// Updated after save button is clicked
	const [homeServer, setHomeServer] = useState('matrix.org');

	// List of available SSO providers
	const [ssoProviders, setSSOProviders] = useState([]);
	const [errorMessage, setErrorMessage] = useState('');

	// Fetches the available login types for a particular homeserver. Defaults to 'matrix.org'
	useEffect(() => {
		const fetchData = async () => {
			const baseUrl = validateAndReturnURL(homeServer);
			const endpoint = "/_matrix/client/v3/login";
			const fullUrl = new URL(endpoint, baseUrl);
			try {
				let response = await axios.get(fullUrl);
				let listOfSSOProviders = [];
				for(let flowItem of response.data.flows){
					if(flowItem.type === 'm.login.sso'){
						listOfSSOProviders = flowItem.identity_providers.map((value) => value.name.toLowerCase());
					}
				}
				setSSOProviders(listOfSSOProviders);
			}
			catch (err) {
				// Still need to handle network errors and URL not found.
				console.log(err.response);
			}
		}
		fetchData();
	}, [homeServer]);

	// Autofills the homeserver field when a user enters a complete and valid matrix user_id.
	async function usernameOnBlur (e) {
		// Regex test for complete user_id
		const pattern = /^@[\w_-]+:\S+/;
		if(!pattern.test(e.target.value)){
			return;
		}
		const userName = e.target.value;
	
		// Extract server name from username
		let server_name = userName.split(':')[1];
		server_name = validateAndReturnURL(server_name);
	
		// Extract host name from server name
		let hostName = new URL(server_name).hostname;
		hostName = validateAndReturnURL(hostName);
	
		const url = new URL('.well-known/matrix/client', hostName);	
		await axios.get(url)
		.then(response => {
			let homeserver_url = response.data['m.homeserver'].base_url;
			if (homeserver_url === undefined){
				throw new Error("Auto Discovery failed due to invalid data");
			}
			homeserver_url = new URL(homeserver_url).hostname;
			setHomeServer(homeserver_url);
			setInputHomeServer(homeserver_url);

			// removes the error message the next time auto discovery is successful
			setErrorMessage('');
		})
		.catch(err => {
			setErrorMessage(err.message);
		});
	}

    return (
	<div>
		<section className="fixed w-full h-full top-0 bg-dark-ash" >

			<div className="text-gray-300 hover:text-white px-4 py-4 font-bold">
                <Link to='/'>matrix-cerberus</Link>
            </div>

			<div className="container mx-auto px-4 h-full">
				<div className="flex content-center items-center justify-center h-full">
					<div className="w-full lg:w-4/12 px-4">
						<div className="relative flex flex-col min-w-0 break-words w-full shadow-lg rounded-lg bg-gray-300 border-0">
							<SSOLogin ssoProviders={ssoProviders} errorMessage={errorMessage} />
						
							<div className="flex-auto px-4 lg:px-10 py-10 pt-0">
								<div className="text-gray-500 text-center mb-3 font-bold">
								
								<small className={ssoProviders.length > 0 ? 'font-semibold' : 'hidden'}>
									Or sign in with credentials
								</small>
								
								</div>
								<form>
									<div className="w-full mb-3">
										<label
										className="block text-gray-700 text-sm font-bold mb-2"
										htmlFor="grid-password"
										>
										Homeserver
										</label>
										<div className='flex items-center justify-between w-full no-overflow'>
											<input
											type="homeserver"
											className="block border-0 px-3 py-3 w-3/4 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring"
											value={inputHomeServer}
											style={{ transition: "all .15s ease" }}
											onChange={(e) => setInputHomeServer(e.target.value)}
											/>
											<div className='flex justify-end w-1/4 ml-4'>
												<button 
												type="button" 
												className="block px-3 py-2.5 bg-gray-900 text-white text-xs font-semibold shadow leading-tight uppercase rounded hover:shadow-lg active:bg-gray-700"
												onClick={() => {setHomeServer(inputHomeServer)}}
												>
													Save
												</button>
											</div>
										</div>
									</div>

									<div className="flex items-center justify-between w-full my-4">
										<label
											className="block text-gray-700 text-xs"
											htmlFor="grid-password"
										>
											Sign in with
										</label>
										<div className="">
											<select value={fieldType} onChange={(e) => setFieldType(e.target.value)} className='block px-1 py-1 rounded-md bg-white shadow border border-solid border-gray-300 text-sm focus:outline-none focus:ring'>
												<option default>Username</option>
												<option value="Email address">Email address</option>
												<option value="Phone">Phone</option>
											</select>
										</div>
									</div>

									<UserField type={fieldType} onBlur={usernameOnBlur}/>
									

									<div className="w-full mb-3">
										<input
										type="password"
										className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
										placeholder="Password"
										style={{ transition: "all .15s ease" }}
										/>
									</div>

									<div className="text-center mt-6">
										<button
										className="bg-gray-900 text-white active:bg-gray-700 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full"
										type="button"
										style={{ transition: "all .15s ease" }}
										>
										Sign In
										</button>
									</div>
								</form>
							</div>
						</div>
					</div>
				</div>
			</div>
		</section>
	</div>
    );
  }
