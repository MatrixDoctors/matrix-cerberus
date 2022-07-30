import React, { useEffect, useState } from 'react'
import PropTypes from "prop-types"

function Table() {
    return (
      <div className='w-full my-2 p-2 bg-gray-300'>
        <div className='flex-col items-center bg-white rounded-md'>
          <div className='w-full p-3 rounded-md border-b border-gray-200 bg-white hover:bg-gray-100'>
            SampleRepo 1
          </div>

          <div className='w-full p-3 rounded-md border-b border-gray-200 bg-white hover:bg-gray-100'>
            SampleRepo 2
          </div>
        </div>
      </div>
    )
}

function InsideButton({type, isTableOpen}) {
    return (
      <div className='w-full my-4 p-2 rounded-md bg-gray-300'>
        <button className="flex justify-start items-center w-full h-10 text-black">
          <div className='flex justify-start w-1/3'>
            <div className='px-4 py-1 mr-2 rounded-lg font-medium'>
              {type}
            </div>
          </div>

          <div className='flex justify-end w-2/3'>
            <svg className="w-4 h-4 ml-3 fill-current" viewBox="0 0 20 20"><path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" fillRule="evenodd"></path></svg>
          </div>
        </button>

        {isTableOpen ? <Table /> : <></>}

      </div>
    )
}

InsideButton.propTypes = {
    type: PropTypes.string,
    isTableOpen: PropTypes.bool
}

export default function UserConditionsDropdown({userName}) {
    const [isOpen, setIsOpen] = useState(false);

    const buttonUI = (
      <button
      className="flex justify-start items-center w-full h-10 border-b border-dark-eye text-black"
      onClick={() => setIsOpen(!isOpen)}
      >
        <div className='flex justify-start items-center w-1/2'>
          <div className='px-4 py-1 mr-2 bg-gray-900 text-white rounded-lg font-medium'>
            User
          </div>

          <div className='mx-2 font-medium'>
            {userName}
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
            <InsideButton type={'Repositories'} isTableOpen={true}/>
            <InsideButton type={'Sponsorship Tiers'} isTableOpen={false}/>
          </div>
        : <></>}
      </div>
    )
  }

UserConditionsDropdown.propTypes = {
    userName: PropTypes.string
}
