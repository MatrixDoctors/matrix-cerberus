import 'react-phone-number-input/style.css'
import PhoneInput from 'react-phone-number-input'

export default function UserField({ type, setUserField, phoneNumber, setPhoneNumber, onUserNameBlur}) {

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
				<div className="flex items-center justify-center mb-3">
					<div className='px-2 py-2 w-full'>
						<PhoneInput
							placeholder="Enter phone number"
							value={phoneNumber}
							onChange={setPhoneNumber}
						/>
					</div>
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
