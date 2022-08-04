import React, { useEffect, useState } from 'react'
import PropTypes from "prop-types"
import Repositories from './Repositories';
import SponsorshipTiers from './SponsorrshipTiers';
import Teams from './Teams';

export default function OrgConditionsDropdown({orgName, roomId}) {
  const [isOpen, setIsOpen] = useState(false);

  const buttonUI = (
    <button
    className="flex justify-start items-center w-full h-10 border-b border-dark-eye text-black"
    onClick={() => setIsOpen(!isOpen)}
    >
      <div className='flex justify-start items-center w-1/2'>
        <div className='px-4 py-1 mr-2 bg-gray-900 text-white rounded-lg font-medium'>
          Org
        </div>

        <div className='mx-2 font-medium'>
          {orgName}
        </div>
      </div>

      <div className='flex justify-end w-1/2'>
        <svg className="w-4 h-4 ml-3 fill-current" viewBox="0 0 20 20"><path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" fillRule="evenodd"></path></svg>
      </div>
    </button>
  );

  return (
    <div className='my-4 p-2 rounded-md'>
      {buttonUI}
      {isOpen
      ? <div className='flex-col items-center w-full bg-white'>
          <Repositories ownerIsUser={false} owner={orgName} roomId={roomId}/>
          <Teams ownerIsUser={false} owner={orgName} roomId={roomId}/>
          <SponsorshipTiers ownerIsUser={false} owner={orgName} roomId={roomId}/>
        </div>
      : <></>}
    </div>
  )
}

OrgConditionsDropdown.propTypes = {
  orgName: PropTypes.string,
  roomId: PropTypes.string
}
