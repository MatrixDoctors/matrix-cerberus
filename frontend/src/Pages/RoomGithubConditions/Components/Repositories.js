import React, { useState } from 'react'
import PropTypes from "prop-types"

function TableRow({repoName}) {
  return (
    <div className='w-full p-3 border-b border-gray-500 bg-gray-300 hover:bg-gray-500 hover:text-white'>
      {repoName}
    </div>
  );
}

TableRow.propTypes = {
  repoName: PropTypes.string
};

export default function Repositories({ownerIsUser, owner}) {
  const [isTableOpen, setIsTableOpen] = useState(false);
  const repoList = ['SampleRepo 1', 'SampleRepo 2'];

  return (
    <div className='w-full my-4 p-2 rounded-md bg-gray-300'>
      <button
      className="flex justify-start items-center w-full h-10 text-black"
      onClick={() => {setIsTableOpen(!isTableOpen)}}
      >
        <div className='flex justify-start w-1/3'>
          <div className='px-4 py-1 mr-2 rounded-lg font-medium'>
            Repositories
          </div>
        </div>

        <div className='flex justify-end w-2/3'>
          <svg className="w-4 h-4 ml-3 fill-current" viewBox="0 0 20 20"><path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" fillRule="evenodd"></path></svg>
        </div>
      </button>

      {isTableOpen
      ? <div className='w-full my-2 p-2 bg-gray-300'>
          <div className='flex-col items-center bg-gray-300 rounded-md'>
            {repoList.map((repo) => {
              return (<TableRow repoName={repo} key={repo} />)
            })}
          </div>
        </div>
      : <></>}

    </div>
  )
};

Repositories.propTypes = {
    ownerIsUser: PropTypes.bool,
    owner: PropTypes.string
}
