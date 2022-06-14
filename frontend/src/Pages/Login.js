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

function AuthButton({ imgUrl}){
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

function UserField({ type }) {
	switch (type) {
		case 'Username': {
			return (
				<div className="w-full mb-3">
					<input
					type="username"
					className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
					placeholder="Username"
					style={{ transition: "all .15s ease" }}
					/>
				</div>
			)
		}

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
	}
}

UserField.propTypes = {
	type: PropTypes.string
}

function SSOLogin({ ssoProviders }) {
	return (
		<div className="rounded-t mb-0 px-6 py-6">
			<div className="text-center mb-3">
			<h6 className="text-gray-600 text-md font-bold">
				{ssoProviders.length > 0 ? 'Sign in with' : 'Sign In'}
			</h6>
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

	const [fieldType, setFieldType] = useState('Username');
	const [inputHomeServer, setInputHomeServer] = useState('matrix.org');
	const [homeServer, setHomeServer] = useState('matrix.org');
	const [ssoProviders, setSSOProviders] = useState([]);

	useEffect(() => {
		const fetchData = async () => {
			const baseUrl = "https://" + homeServer;
			const endpoint = "/_matrix/client/v3/login";
			const fullUrl = new URL(endpoint, baseUrl);

			let response = await axios.get(fullUrl);
			let listOfSSOProviders = [];
			for(let flowItem of response.data.flows){
				if(flowItem.type === 'm.login.sso'){
					listOfSSOProviders = flowItem.identity_providers.map((value) => value.name.toLowerCase());
				}
			}
			setSSOProviders(listOfSSOProviders);
		}
		fetchData();
	}, [homeServer]);

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
							<SSOLogin ssoProviders={ssoProviders}/>
						
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

									<UserField type={fieldType}/>
									

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
