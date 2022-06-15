export default function UserField({ type, setUserField , onUserNameBlur }) {
	switch (type) {
		case 'Email address': {
			return (
				<div className="w-full mb-3">
					<input
					type="email"
					className="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
					placeholder="Email"
					style={{ transition: "all .15s ease" }}
					onChange={(e) => setUserField(e.target.value)}
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
					onBlur={onUserNameBlur}
					onChange={(e) => setUserField(e.target.value)}
					/>
				</div>
			)
		} 
	}
}
