import React from 'react'
import PropTypes from 'prop-types'
import 'react-phone-number-input/style.css'
import PhoneInput from 'react-phone-number-input'

export default function UserField({ styleClassForFields, type, setUserField, disableFields, phoneNumber, setPhoneNumber, onUserNameBlur}) {

	switch (type) {
		case 'Email address': {
			return (
				<div className="w-full mb-3">
					<input
					disabled={disableFields}
					type="email"
					className={styleClassForFields}
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
							disabled={disableFields}
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
					disabled={disableFields}
					type="username"
					className={styleClassForFields}
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

UserField.propTypes = {
	styleClassForFields: PropTypes.string,
	type: PropTypes.string,
	setUserField: PropTypes.any,
	disableFields: PropTypes.bool,
	phoneNumber: PropTypes.string,
	setPhoneNumber: PropTypes.any,
	onUserNameBlur: PropTypes.any
}
