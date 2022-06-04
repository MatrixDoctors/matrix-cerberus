import React, { useState } from 'react'
import { Link } from 'react-router-dom'

function AuthButton({ imgUrl, name }){
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

export default function Login() {

	const [fieldType, setFieldType] = useState('Username');

	function handleChange(e) {
		setFieldType(e.target.value);
	}

    return (
	<div>
		<section className="fixed w-full h-full top-0" style={{ backgroundColor: "#161b22"}}>
			
			<div className="text-gray-300 hover:text-white px-4 py-4 font-bold">
                <Link to='/'>matrix-cerberus</Link>
            </div>

			<div className="container mx-auto px-4 h-full">
				<div className="flex content-center items-center justify-center h-full">
					<div className="w-full lg:w-4/12 px-4">
						<div className="relative flex flex-col min-w-0 break-words w-full shadow-lg rounded-lg bg-gray-300 border-0">
							<div className="rounded-t mb-0 px-6 py-6">
								<div className="text-center mb-3">
								<h6 className="text-gray-600 text-sm font-bold">
									Sign in with
								</h6>
								</div>

								{/* Button Wrapper */}
								<div className="btn-wrapper flex items-center justify-center">
								<AuthButton imgUrl={require("../assets/img/github.svg").default} name={"github"}/>
								<AuthButton imgUrl={require("../assets/img/google.svg").default} name={"google"}/>
								<AuthButton imgUrl={require("../assets/img/gitlab.svg").default} name={"gitlab"}/>
								<AuthButton imgUrl={require("../assets/img/facebook.svg").default} name={"facebook"}/>
								<AuthButton imgUrl={require("../assets/img/apple.svg").default} name={"apple"}/>
								</div>
								<hr className="mt-6 border-b-1 border-gray-400" />
							</div>
						
							<div className="flex-auto px-4 lg:px-10 py-10 pt-0">
								<div className="text-gray-500 text-center mb-3 font-bold">
								<small>Or sign in with credentials</small>
								</div>
								<form>
								<div className="w-full mb-3">
									<label
									className="block text-gray-700 text-sm font-bold mb-2"
									htmlFor="grid-password"
									>
									Homeserver
									</label>
									<input
									type="email"
									className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
									placeholder="matrix.org"
									style={{ transition: "all .15s ease" }}
									/>
								</div>

								<div className="flex items-center justify-between w-full my-4">
									<label
										className="block text-gray-700 text-xs"
										htmlFor="grid-password"
									>
										Sign in with
									</label>
									<div className="">
										<select value={fieldType} onChange={handleChange} className='block px-1 py-1 rounded-md bg-white shadow border border-solid border-gray-300 text-sm focus:outline-none focus:ring'>
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
