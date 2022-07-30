import React from 'react'
import PropTypes from "prop-types"

export default function SponsorshipTiers({ownerIsUser, owner}) {
  return (
    <div className='w-full my-4 p-2 rounded-md bg-gray-300'>
      <button className="flex justify-start items-center w-full h-10 text-black">
        <div className='flex justify-start w-1/3'>
          <div className='px-4 py-1 mr-2 rounded-lg font-medium'>
            Sponsorship Tiers
          </div>
        </div>

        <div className='flex justify-end w-2/3'>
          <svg className="w-4 h-4 ml-3 fill-current" viewBox="0 0 20 20"><path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" fillRule="evenodd"></path></svg>
        </div>
      </button>

    </div>
  )
};

SponsorshipTiers.propTypes = {
    ownerIsUser: PropTypes.bool,
    owner: PropTypes.string
}
