import React from 'react'

export default function AccountSettings() {

	return (
		<div>  
			<div className="flex items-center w-full h-48 py-5 shadow-lg" 
				style={{ backgroundColor: "#0d1117" }} 
			>
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
									Kuries
								</div>
							</div>

							<hr className="border-b-1 border-gray-300" />
							
							<div className='flex items-center w-full my-3'>	
								<div className='w-1/3 text-gray-600 font-semibold'>
									Homeserver
								</div>
								<div className='w-2/3 px-2 text-gray-600'>
									matrix.org
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
									Connected as kuries
								</div>
								<div className='flex justify-end mx-2 w-1/3'>
									<span className='px-2 text-blue-600 hover:shadow-md'>
										Edit
									</span>
								</div>
								
							</div>

							<hr className="border-b-1 border-gray-300" />

							<div className='flex items-center w-full my-3'>
								<div className='flex items-center w-1/3'>
									<div
										className="inline-block h-5 w-5 mx-2 rounded-full overflow-hidden"
										type="button"
										style={{ transition: "all .15s ease" }}
									>
										<img
										alt="..."
										className="h-full w-full mr-1"
										src={require("../assets/img/gitlab.svg").default}
										/>
									</div>
									<div className='inline-block text-gray-600 font-semibold'>
										Gitlab
									</div>
								</div>
								<div className='w-1/3 px-2 text-gray-600'>
									Connected as Binesh
								</div>
								<div className='flex justify-end mx-2 w-1/3'>
									<span className='px-2 text-blue-600 hover:shadow-md'>
										Edit
									</span>
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
