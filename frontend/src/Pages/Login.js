import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import UserField from '../Components/UserField'
import SSOLogin from '../Components/SSOLogin'
import {parsePhoneNumber} from "react-phone-number-input"
import validateAndReturnUrl from '../HelperFunctions/validateAndReturnUrl'
import axios from 'axios'

/**
 * Login page which authenticates a user with the backend for a chosen matrix homeserver.
 * OpenID tokens are used for authentication.
 */
export default function Login() {

	const styles = {
		transition: "all .15s ease"
	};

	const default_homeserver = 'matrix.org';
	localStorage.setItem("homeServer", "https://matrix.org");

	// Used to set the Identifier type for password based login
	const [fieldType, setFieldType] = useState('Username');
	const [userField, setUserField] = useState('');

	// State variable to store the complete phone number including the country calling code without '+'.
	//Ex: 919676765xxxxx (India:- +91)
	const [phoneNumber, setPhoneNumber] = useState('');

	const [password, setPassword] = useState('');

	const [inputHomeServer, setInputHomeServer] = useState('matrix.org');

	// Updated after save button is clicked
	const [homeServer, setHomeServer] = useState(default_homeserver);

	const [ssoProviders, setSSOProviders] = useState([]);
	const [errorMessage, setErrorMessage] = useState('');

	// Enable save button in homeserver when the inputHomeServer is being changed
	// and Disable it when the save button is clicked.
	const [disableSave, setDisableSave] = useState(true);

	// Used to disable input fields when the homeserver url is invalid.
	const [disableFields, setDisableFields] = useState(false);

	// Fetches the available login types for a particular homeserver. Defaults to 'matrix.org'
	useEffect(() => {
		const fetchData = async () => {
			try {
				const baseUrl = validateAndReturnUrl(homeServer);
				const endpoint = "/_matrix/client/v3/login";
				const fullUrl = new URL(endpoint, baseUrl);

				let response = await axios.get(fullUrl);
				let listOfSSOProviders = [];
				for(let flowItem of response.data.flows){
					if(flowItem.type === 'm.login.sso'){
						listOfSSOProviders = flowItem.identity_providers;
					}
				}
				setSSOProviders(listOfSSOProviders);
				setDisableFields(false);
				setErrorMessage('');

				localStorage.setItem('homeServer', baseUrl);
			}
			catch (err) {
				if (err.message === 'Network Error') {
					setErrorMessage('Invalid Homeserver URL');
				}
				else{
					setErrorMessage(err.message);
				}
				setDisableFields(true);
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
		server_name = validateAndReturnUrl(server_name);

		// Extract host name from server name
		let hostName = new URL(server_name).hostname;
		hostName = validateAndReturnUrl(hostName);

		const url = new URL('.well-known/matrix/client', hostName);
		await axios.get(url)
		.then(response => {
			let homeserver_url = response.data['m.homeserver'].base_url;
			if (homeserver_url === undefined){
				throw new Error();
			}
			homeserver_url = new URL(homeserver_url).hostname;
			setHomeServer(homeserver_url);
			setInputHomeServer(homeserver_url);

			localStorage.setItem('homeServer', homeserver_url);
			// Removes the error message the next time auto discovery is successful
			setErrorMessage('');
		})
		.catch(err => {
			setErrorMessage("Invalid homeserver directory response");
		});
	}

	async function handleSignInClick() {

		// Homeserver url is invalid
		if(disableFields){
			return;
		}

		if(userField === '' || password === ''){
			setErrorMessage("Input Fields are empty");
			return;
		}

		let identifier;

		let phone, country;
		if(fieldType === 'Phone'){
			const intlPhoneObject = parsePhoneNumber(phoneNumber);
			const callingCode = '+' + intlPhoneObject.countryCallingCode;
			phone = phoneNumber.replace(callingCode, '');
			country = intlPhoneObject.country;
			console.log(country);
		}

		switch (fieldType) {
			case 'Email address':
				identifier = {
					"type": "m.id.thirdparty",
					"medium": "email",
					  "address": userField
				};
				break;
			case 'Phone':
				identifier = {
					"type": "m.id.phone",
					"country": country,
					"phone": phone,
					"number": phone
				}
				break;
			default:
				identifier = {
					"type": "m.id.user",
					  "user": userField
				}
		}
		const baseUrl = validateAndReturnUrl(homeServer);
		const fullUrl = new URL('/_matrix/client/v3/login', baseUrl);
		await axios.post(fullUrl, {
			type: "m.login.password",
			identifier: identifier,
			password: password
		})
		.then((resp) => {
			const userId = resp.data.user_id;
			setErrorMessage(`You have logged in as ${userId}`);
		})
		.catch( (err) => {
			// Login attempt has failed. The provided authentication data was incorrect.
			if(err.response.status === 403){
				setErrorMessage("Incorrect credentials")
			}
		})
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
							{/* First half of login componenet */}
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
								<SSOLogin ssoProviders={ssoProviders} />
								<hr className="mt-6 border-b-1 border-gray-400" />
							</div>

							{/* Second half of login componenet */}
							<div className="flex-auto px-4 lg:px-10 py-10 pt-0">
								<div className="text-gray-500 text-center mb-3 font-bold">

								<small className={ssoProviders.length > 0 ? 'font-semibold' : 'hidden'}>
									Or sign in with credentials
								</small>

								</div>
								<form>
									{/* Homeserver componenet */}
									<div className="w-full mb-3">
										<label
										className="block text-gray-700 text-sm font-bold mb-2"
										htmlFor="grid-password"
										>
										Homeserver
										{/* border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full disabled:opacity-50 */}
										</label>
										<div className='flex items-center justify-between w-full no-overflow'>
											<input
											type="homeserver"
											className="field-input w-3/4"
											value={inputHomeServer}
											style={styles}
											onChange={(e) => {
												e.preventDefault();
												setInputHomeServer(e.target.value);
												setDisableSave(!e.target.value);
											}}/>
											<div className='flex justify-end w-1/4 ml-4'>
												<button
												type="button" disabled={disableSave}
												className="block px-3 py-2.5 bg-gray-900 text-white text-xs font-semibold shadow leading-tight uppercase rounded hover:shadow-lg hover:bg-gray-800 disabled:opacity-20"
												onClick={() => {
													setHomeServer(inputHomeServer);
													setDisableSave(true);
												}}>
													Save
												</button>
											</div>
										</div>
									</div>
									{/* Select option for password based identifiers */}
									<div className="flex items-center justify-between w-full my-4">
										<label
											className="block text-gray-700 text-xs"
											htmlFor="grid-password"
										>
											Sign in with
										</label>
										<div className="">
											<select
											disabled={disableFields}
											value={fieldType}
											onChange={(e) => setFieldType(e.target.value)}
											className='block px-1 py-1 rounded-md bg-white shadow border border-solid border-gray-300 text-sm focus:outline-none focus:ring disabled:opacity-50'
											>
												<option default value="Username">Username</option>
												<option value="Email address">Email address</option>
												<option value="Phone">Phone</option>
											</select>
										</div>
									</div>

									<UserField type={fieldType} setUserField={setUserField} disableFields={disableFields} phoneNumber={phoneNumber} setPhoneNumber={setPhoneNumber} onUserNameBlur={usernameOnBlur} />

									{/* Password field */}
									<div className="w-full mb-3">
										<input
										disabled={disableFields}
										type="password"
										className='field-input w-full'
										placeholder="Password"
										style={styles}
										onChange={(e) => setPassword(e.target.value)}
										/>
									</div>
									{/* Sign in button */}
									<div className="text-center mt-6">
										<button
										className="bg-gray-900 text-white active:bg-gray-700 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full"
										type="button"
										style={styles}
										onClick={handleSignInClick}
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
