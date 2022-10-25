import React, { useContext } from 'react'
import Helmet from 'react-helmet';
import { GlobalContext } from '../GlobalContext';
import axios from '../HelperFunctions/customAxios';

/**
 * The default web page where an authorized matrix user can edit their third-party account connections.
 */
export default function AccountSettings() {
	const {matrixUserId, githubUserId, patreonUserId} = useContext(GlobalContext);
	const homeServer = localStorage.getItem('homeServer');

	function oauthHandleClick(accountType){
		axios.get(`/api/${accountType}/login`)
		.then( (resp) => {
			localStorage.setItem('state', resp.data.state);
			window.location.href = resp.data.url;
		})
		.catch(err => {
			console.error(err);
		});
	}

	return (
		<div>
			<Helmet>
				<title>Accounts - MatrixCerberus</title>
        	</Helmet>

			<div className="flex items-center w-full h-48 py-5 shadow-lg bg-dark-eye" >
				<div className='flex items-center justify-center w-full sm:w-1/3'>
					<div className='relative bottom-5 font-bold text-3xl my-5 px-3 sm:px-0 text-gray-200'>
						Accounts
					</div>
				</div>
				<div className='hidden sm:w-2/3 sm:block'/>
			</div>
			<div className="container mx-auto px-4 h-full">
				<div className="flex content-center items-center justify-center h-full ">
					<div className='lg:w-1/6 bg-gray-900' />
					<div className="w-full lg:w-4/6 px-4 ">
						<div className="relative bottom-10 rounded-t mb-0 px-6 py-6 bg-gray-100 hover:shadow-xl">

							{/* Account Information */}
							<h6 className="block mb-6 text-gray-800 font-bold">
								Account Information
							</h6>
							<div className='flex items-center w-full mb-3'>
								<div className='w-1/3 text-gray-600 font-semibold'>
									Matrix ID
								</div>
								<div className='w-2/3 px-2 text-gray-600'>
									{matrixUserId}
								</div>
							</div>

							<hr className="border-b-1 border-gray-300" />

							<div className='flex items-center w-full my-3'>
								<div className='w-1/3 text-gray-600 font-semibold'>
									Homeserver
								</div>
								<div className='w-2/3 px-2 text-gray-600'>
									{homeServer}
								</div>
							</div>

							<hr className="border-b-1 border-gray-300" />

							{/* Third party accounts */}
							<h6 className="block my-6 text-gray-800 font-bold">
								Third Party Accounts
							</h6>
							<div className='flex items-center justify-between w-full mb-3'>
								<div className='flex items-center w-1/3'>
									<div
										className="inline-block h-5 w-5 mx-2 rounded-full overflow-hidden"
										type="button"
										style={{ transition: "all .15s ease" }}
									>
										<img
										alt="..."
										className="h-full w-full mr-1"
										src={require("../assets/img/github.svg").default}
										/>
									</div>
									<div className='inline-block text-gray-600 font-semibold'>
										Github
									</div>
								</div>
								<div className='inline-block px-2 w-1/3 text-gray-600'>
									{githubUserId == "" ? "Disconnected" : `${githubUserId}`}
								</div>
								<div className='flex justify-end mx-2 w-1/3'>
									<button
									onClick={() => oauthHandleClick('github')}
									className='px-2 inline text-blue-600 hover:shadow-md'>
										{githubUserId == "" ? "Connect" : "Edit"}
									</button>
								</div>

							</div>

							<hr className="border-b-1 border-gray-300" />

							<div className='flex items-center w-full my-3'>
								<div className='flex items-center w-1/3'>
									<div
										className="inline-block h-4 w-4 mx-2"
										type="button"
										style={{ transition: "all .15s ease" }}
									>
										<img
										alt="..."
										className="h-full w-full mr-1"
										src={require("../assets/img/patreon.svg").default}
										/>
									</div>
									<div className='inline-block text-gray-600 font-semibold'>
										Patreon
									</div>
								</div>
								<div className='w-1/3 px-2 text-gray-600'>
									{patreonUserId == "" ? "Disconnected" : `${patreonUserId}`}
								</div>
								<div className='flex justify-end mx-2 w-1/3'>
								<button
									onClick={() => oauthHandleClick('patreon')}
									className='px-2 inline text-blue-600 hover:shadow-md'>
										{patreonUserId == "" ? "Connect" : "Edit"}
									</button>
								</div>
							</div>

							<hr className="my-1 border-b-1 border-gray-300" />
						</div>
					</div>
					<div className='lg:w-1/6 bg-gray-900' />
				</div>
			</div>
		</div>
	)
	}
