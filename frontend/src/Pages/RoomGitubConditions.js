import React from 'react'
import Helmet from 'react-helmet'
import { Link, useParams } from 'react-router-dom'

export default function RoomGitubConditions() {
  const { roomId } = useParams();

  const buttonUserUI = (
      <button className="flex justify-start items-center w-full h-10 px-5 text-black hover:bg-gray-400">
        <div className='flex justify-start items-center w-1/2'>
          <div className='px-4 py-1 mr-2 bg-gray-900 text-white rounded-lg font-medium'>
            User
          </div>

          <div className='mx-2 font-medium'>
            Kuries
          </div>
        </div>

        <div className='flex justify-end w-1/2'>
          <svg className="w-4 h-4 ml-3 fill-current" viewBox="0 0 20 20"><path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" fillRule="evenodd"></path></svg>
        </div>
      </button>
  );

  const buttonOrgUI = (
    <button className="flex justify-start items-center w-full h-10 px-5 text-black">
      <div className='flex justify-start items-center w-1/2'>
        <div className='px-4 py-1 mr-2 bg-gray-900 text-white rounded-lg font-medium'>
          Org
        </div>

        <div className='mx-2 font-medium'>
          TestOrgForCerberus
        </div>
      </div>

      <div className='flex justify-end w-1/2'>
        <svg className="w-4 h-4 ml-3 fill-current" viewBox="0 0 20 20"><path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" fillRule="evenodd"></path></svg>
      </div>
    </button>
);

  return (
    <>
      <Helmet>
        <title>Github Conditions - MatrixCerberus</title>
      </Helmet>

      <div className="flex flex-col sm:flex-row items-center justify-around w-full h-48 py-5 shadow-lg bg-dark-eye" >
          <div className='flex w-full justify-center'>
              <div className="hidden sm:w-1/4 sm:block"/>
              <div className='sm:w-3/4 relative font-bold text-2xl m-5 px-3 sm:px-0 text-gray-200'>
                  Github Conditions
              </div>
          </div>

          <div className='flex w-full items-center justify-center sm:justify-end sm:mr-4'>
              <Link to={`/rooms/${roomId}`} >
                  <button className="block m-3 px-6 py-3 bg-indigo-700 hover:bg-indigo-600 focus:outline-none rounded">
                      <div className="text-sm font-medium leading-none text-white">
                          Back to Room page
                      </div>
                  </button>
              </Link>
          </div>
      </div>

      <div className="w-full px-6 lg:mx-auto lg:w-10/12">
        <div className="w-full my-3 px-4 pt-4 pb-5 overflow-y-auto">
          <div className='my-4 p-2 bg-gray-200 border border-dark-eye rounded-md hover:bg-gray-400'>
            {buttonUserUI}
          </div>

          <div className='my-4 p-2 bg-gray-200 border border-dark-eye rounded-md hover:bg-gray-400'>
            {buttonOrgUI}
          </div>

          <div className='my-4 p-2 bg-gray-200 border border-dark-eye rounded-md hover:bg-gray-400'>
            {buttonOrgUI}
          </div>
        </div>
      </div>
    </>
  )
}
