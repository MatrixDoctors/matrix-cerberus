import React from 'react'
import PropTypes from 'prop-types'
import 'react-phone-number-input/style.css'
import PhoneInput from 'react-phone-number-input'

export default function UserField({ type, setUserField, disableFields, phoneNumber, setPhoneNumber, onUserNameBlur}) {
	const styles = {
		transition: "all .15s ease"
	};

	switch (type) {
		case 'Email address': {
			return (
				<div className="w-full mb-3">
					<input
					disabled={disableFields}
					aria-label="email"
					type="email"
					className="field-input w-full"
					placeholder="Email"
					style={styles}
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
							aria-label="phone-number"
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
					aria-label='Username'
					className="field-input w-full"
					placeholder="Username"
					style={styles}
					onBlur={onUserNameBlur}
					onChange={(e) => setUserField(e.target.value)}
					/>
				</div>
			)
		}
	}
}

UserField.propTypes = {
	type: PropTypes.string,
	setUserField: PropTypes.func,
	disableFields: PropTypes.bool,
	phoneNumber: PropTypes.string,
	setPhoneNumber: PropTypes.func,
	onUserNameBlur: PropTypes.func
}
