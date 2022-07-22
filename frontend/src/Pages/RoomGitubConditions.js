import React from 'react'
import Helmet from 'react-helmet'
import { Link, useParams } from 'react-router-dom'

export default function RoomGitubConditions() {
  const { roomId } = useParams();

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
    </>
  )
}
